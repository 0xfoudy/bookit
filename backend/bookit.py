import datetime
from dotenv import load_dotenv
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)


def main():

    # Load environment variables from .env file
    load_dotenv()

    # Now you can use the environment variable
    openai_api_key = os.environ.get('OPENAI_API_KEY')

    current_date = datetime.date.today()

    llm = ChatOpenAI(model_name='gpt-3.5-turbo',
                temperature = 0,
                max_tokens = 256,
                openai_api_key=openai_api_key)

    # Prompt
    template = """You are a customers' assistant named Kate, booking reservations for a restaurant, today is {current_date}
    Take the folowing user input: {{query}}, confirm with the client his intent (options are restricted to new reservation, reservation modification, or asking a general question about the restaurant)
    Extract the mentioned date, find the number of available tables and ask for the name of the person reserving.
    
    Sum up the conversation by repeating the collected details in the following:
    Name:
    Number of persons:
    Date and Time:
    
    Finalize with 'Thank you for your reservation!'""".format(current_date=current_date)

    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template="{query}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt,human_message_prompt])
    
    # prompt = ChatPromptTemplate(
    #     messages=[
    #         SystemMessagePromptTemplate.from_template(
    #             """You are a customers' assistant named Kate, booking reservations for a restaurant, today is the 12th of December"
    # Take the folowing user input: {text}
    
    # Extract the mentioned date, find the number of available tables and ask for reservation details.
    
    # Sum up the conversation by repeating the collected details in the following:
    # Name:
    # Number of persons:
    # Date and Time:
    
    # Finalize with 'Thank you for your reservation!'"""
    #         ),
    #         # The `variable_name` here is what must align with memory
    #         MessagesPlaceholder(variable_name="chat_history"),
    #         HumanMessagePromptTemplate.from_template("{text}"),
    #     ]
    # )
    # 
    #    # Notice that we `return_messages=True` to fit into the MessagesPlaceholder
    # Notice that `"chat_history"` aligns with the MessagesPlaceholder name
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    #conversation = LLMChain(llm=llm, prompt=prompt, verbose=True, memory=memory)

    # Notice that we just pass in the `question` variables - `chat_history` gets populated by memory
   # conversation({"text": "hi"})
   # print(conversation({"text": "I would like to book a table tomorrow evening"}))

    def get_response(query):
        chain = LLMChain(llm=llm, prompt=chat_prompt, memory = memory)
        response = chain.run(query)

        return response

    # conversation flow
    conversation = []
    while True:
        query = input("Human: ")
        conversation.append('User: ' + query)

        output = get_response(query)
        conversation.append('Bookit: ' + output)

        print(output)


if __name__ == "__main__": 
    main()