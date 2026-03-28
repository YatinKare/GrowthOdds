from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent

write_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="write_agent",
    description="write marketing content",
    instruction="""
        You are a startup-savy X (twitter) post content generator.
        Based **only** on the user's request and the past marketing experiment reccomendations: {{past_experiements_reccomendations}}, write a 250 character post about the user's topic.
        Output **ONLY** the content of the post.
        Do not add any text before or after the content of the post.
    """,
    output_key="post_content",
)

past_experiements_considerations_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="past_experiements_considerations_agent",
    description="Summerize past considerations",
    instruction="""
        You are a great lead marketing manager.
        With the past experiements, create 3 tips for improving users and clicks for next time.
    """,
    output_key="past_experiements_reccomendations",
)

generate_reccomendations_agent = SequentialAgent(
    name="generate_reccomendations_agent",
    description="generates marketing content",
    sub_agents=[past_experiements_considerations_agent, write_agent],
)

root_agent = generate_reccomendations_agent
