from typing import Optional

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

from src.core.interview.interview_manager_state import InterviewManagerStateInterface, InterviewManagerStateBase
from src.core.interview.resume_validation_state import InterviewManagerResumeValidationState
from src.core.prompts.interview.extract_resume_info import extract_resume_info_prompt_template
from src.core.prompts.interview.introduction import get_resume_message
from src.domain.models.message import Message, MessageType
from src.domain.models.resume_info import ResumeInfo
from src.domain.models.session import SessionState
from src.infrastructure.llm import claude_sonnet


class InterviewManagerResumeState(InterviewManagerStateInterface, InterviewManagerStateBase):
    def __init__(self, change_state, session):
        super().__init__(change_state=change_state, session=session)

    @staticmethod
    def get_init_message() -> Optional[Message]:
        return Message(
            content=get_resume_message,
            type=MessageType.SYSTEM
        )

    @staticmethod
    def get_session_state() -> SessionState:
        return SessionState.RESUME

    async def handle_message(self, message: Optional[str]):
        parser = PydanticOutputParser(pydantic_object=ResumeInfo)
        format_instructions = parser.get_format_instructions()
        extract_resume_info_chain = ((PromptTemplate(
            input_variables=["resume_text"],
            partial_variables={"format_instructions": format_instructions},
            template=extract_resume_info_prompt_template
        )) | claude_sonnet() | parser)

        # TODO: error handling here
        resume_info: ResumeInfo = extract_resume_info_chain.invoke({
            "resume_text": message
        })
        # TODO: resume info should be saved to session
        print(resume_info.years_of_experience)

        target_state = InterviewManagerResumeValidationState(session = self.session, change_state=self.change_state)
        self.change_state(target_state)

        return target_state.get_init_message()
