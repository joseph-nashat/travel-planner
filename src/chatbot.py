import dotenv
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

dotenv.load_dotenv()

chat = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)

questionList = [
                    "Great. What is your departure location ? ",
                        "And what is yout distination location",
                        "Greet choise , when are you planning to travel please provied the date in yyyy-mm-dd for better experiance?",
                        "how long you are ganne to stay ",
                        "how many paople gonne travel including you",
                        "Alright , what is the budget for the trip?",
                        "transporter type you prefere to use in the trip=> car , bus ,...",
                        "activit types and interests (beach, mountains, culture, adventure, etc.)",
                        "cuisine type",
                        "anything alse you want to add a note any kind of activity or anything i should consider"]
template =  """ 
            you are an intelligent AI assistant that tailors vacation plans based on a user's preferences,past travels, budget, and more 
                    captures essential user details: travel history, interests (beach, mountains, culture, adventure, etc.), dietary restrictions, budget, and other preferences to make informed suggestions.
                    note you should just ask one question each time
                    note you should use user name when he provied it 
                    using a set of question 
                    note you should ask one question at a time and wait for the user response to generate another response
                    in the plan you should consider the weather and suggest any local event and which airport they should talk and any near hotal and try to hightlight the budget of the activitas
                    {questionList}
                    please rephrase them and generate as much question as you need to have all the data to plan                                     
                    Here is the user input {input}     
                    Given the below chat history between you and user {history}           
"""

promptV1 = ChatPromptTemplate.from_template(template)
#Partial assign values from code not from user
promptV1 = promptV1.partial(questionList=questionList)


promptV2 = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """ 
            you are an intelligent AI assistant that tailors vacation plans based on a user's preferences,past travels, budget, and more 
                    captures essential user details: travel history, interests (beach, mountains, culture, adventure, etc.), dietary restrictions, budget, and other preferences to make informed suggestions.
                    note you should just ask one question each time
                    note you should use user name when he provied it 
                    using a set of question 
                    note you should ask one question at a time and wait for the user response to generate another response
                    in the plan you should consider the weather and suggest any local event and which airport they should talk and any near hotal and try to hightlight the budget of the activitas
                    [
                    "Great. What is your departure location ? ",
                        "And what is yout distination location",
                        "Greet choise , when are you planning to travel please provied the date in yyyy-mm-dd for better experiance?",
                        "how long you are ganne to stay ",
                        "how many paople gonne travel including you",
                        "Alright , what is the budget for the trip?",
                        "transporter type you prefere to use in the trip=> car , bus ,...",
                        "activit types and interests (beach, mountains, culture, adventure, etc.)",
                        "cuisine type",
                        "anything alse you want to add a note any kind of activity or anything i should consider"]
                    please rephrase them and generate as much question as you need to have all the data to plan
                    
                    
                    """,
       
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)





def callChatBotV1(q,h=""):
    chain = promptV1 | chat
    res=chain.invoke({"input": q,"history":h})
    return res.content

def callChatBotV2(q):
    chain = promptV2 | chat
    res=chain.invoke(
    {
        "messages": [
            HumanMessage(
                content=f"{q}"
            ),
            #AIMessage(content="J'adore la programmation."),
            #HumanMessage(content="What did you just say?"),
        ],
    })
    return res.content