from agents.config import OPERATION_SYSTEM

OPERATION_SYSTEM_AGENT_NAME = "Operation System"
PROJECT_MANAGER_AGENT_NAME = "Project Manager"
DEVELOPER_SPECIALIST_AGENT_NAME = "Developer Specialist"
RESEARCH_AGENT_NAME = "Research"
SOFTWARE_ENGINEER_AGENT_NAME = "Software Engineer"
EVERYONE = "Everyone"
USER_NAME = "User"

AGENTS_DESCRIPTIONS = {

    USER_NAME: "This agent is the user (real person) who is expert in software engineering and needs help from the "
               "system to create their solution for the stake holders.",

    PROJECT_MANAGER_AGENT_NAME: "Manage the project. When interacting with the user, suggest system architecture, "
            "such as system requirements, programming language, etc. Given a message from the user, this agent"
            " can ask for more details about the project. Consider that the user is a software engineer expert."
            "Also, this agent can manage the database, given the available actions to be performed, such as "
            "creating a new epoch (the main project description), create stories, create tasks, delete, etc. Finally, "
            "this agent can ask for other agents to do other activities, such as research, generate artefact or "
            "solve a task.",

    OPERATION_SYSTEM_AGENT_NAME: f"Given a description of possible actions, this agent handle {OPERATION_SYSTEM} operation system."
            f"This agent receives commands from the {DEVELOPER_SPECIALIST_AGENT_NAME} agent most of the time. This agent "
            "can perform task such as configuring the environment, set variables, install packages, manage folders, "
            "create files, etc. Any action performed in the operation system, as mentioned previously is done only "
            "by this agent, so, the other agents must ask to this agent in order to perform them.",

    RESEARCH_AGENT_NAME: "This agent is responsible for perform research on the internet and bring a summary of the result. So, "
            "other agents might need to retrieve external information to complete a task, such as making decision, check "
            "resolution for errors, etc.",

    SOFTWARE_ENGINEER_AGENT_NAME: f"This agent is responsible for resolve tasks given by the {PROJECT_MANAGER_AGENT_NAME} "
                            f"agent. This agent can read the task specification from the database and command "
                            f"{OPERATION_SYSTEM_AGENT_NAME}, {RESEARCH_AGENT_NAME}, and {DEVELOPER_SPECIALIST_AGENT_NAME}." ,

    DEVELOPER_SPECIALIST_AGENT_NAME: "This agent is responsible for development artfacts software based in specifications received,"
                                      'however will need the code with quality and conformity need to make requests sended,' 
                                      f"This agent can be communication with: {RESEARCH_AGENT_NAME},{SOFTWARE_ENGINEER_AGENT_NAME},{PROJECT_MANAGER_AGENT_NAME}."
}
