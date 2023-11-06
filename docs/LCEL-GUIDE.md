
# Cookbook

In this notebook we'll take a look at a few common types of sequences to
create.

## PromptTemplate + LLM​

A PromptTemplate -> LLM is a core chain that is used in most other larger
chains/systems.

    
    
    from langchain.prompts import ChatPromptTemplate  
    from langchain.chat_models import ChatOpenAI  
    

#### API Reference:

  * ChatPromptTemplate from `langchain.prompts`
  * ChatOpenAI from `langchain.chat_models`

    
    
        /Users/harrisonchase/.pyenv/versions/3.9.1/envs/langchain/lib/python3.9/site-packages/deeplake/util/check_latest_version.py:32: UserWarning: A newer version of deeplake (3.6.14) is available. It's recommended that you update to the latest version using `pip install -U deeplake`.  
          warnings.warn(  
    
    
    
    model = ChatOpenAI()  
    
    
    
    prompt = ChatPromptTemplate.from_template("tell me a joke about {foo}")  
    
    
    
    chain = prompt | model  
    
    
    
    chain.invoke({"foo": "bears"})  
    
    
    
        AIMessage(content='Why don\'t bears use cell phones? \n\nBecause they always get terrible "grizzly" reception!', additional_kwargs={}, example=False)  
    

Often times we want to attach kwargs to the model that's passed in. Here's a
few examples of that:

### Attaching Stop Sequences​

    
    
    chain = prompt | model.bind(stop=["\n"])  
    
    
    
    chain.invoke({"foo": "bears"})  
    
    
    
        AIMessage(content="Why don't bears use cell phones?", additional_kwargs={}, example=False)  
    

### Attaching Function Call information​

    
    
    functions = [  
        {  
          "name": "joke",  
          "description": "A joke",  
          "parameters": {  
            "type": "object",  
            "properties": {  
              "setup": {  
                "type": "string",  
                "description": "The setup for the joke"  
              },  
              "punchline": {  
                "type": "string",  
                "description": "The punchline for the joke"  
              }  
            },  
            "required": ["setup", "punchline"]  
          }  
        }  
      ]  
    chain = prompt | model.bind(function_call= {"name": "joke"}, functions= functions)  
    
    
    
    chain.invoke({"foo": "bears"}, config={})  
    
    
    
        AIMessage(content='', additional_kwargs={'function_call': {'name': 'joke', 'arguments': '{\n  "setup": "Why don\'t bears wear shoes?",\n  "punchline": "Because they have bear feet!"\n}'}}, example=False)  
    

## PromptTemplate + LLM + OutputParser​

We can also add in an output parser to easily trasform the raw LLM/ChatModel
output into a more workable format

    
    
    from langchain.schema.output_parser import StrOutputParser  
    

#### API Reference:

  * StrOutputParser from `langchain.schema.output_parser`

    
    
    chain = prompt | model | StrOutputParser()  
    

Notice that this now returns a string - a much more workable format for
downstream tasks

    
    
    chain.invoke({"foo": "bears"})  
    
    
    
        "Why don't bears wear shoes?\n\nBecause they have bear feet!"  
    

### Functions Output Parser​

When you specify the function to return, you may just want to parse that
directly

    
    
    from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser  
    chain = (  
        prompt   
        | model.bind(function_call= {"name": "joke"}, functions= functions)   
        | JsonOutputFunctionsParser()  
    )  
    

#### API Reference:

  * JsonOutputFunctionsParser from `langchain.output_parsers.openai_functions`

    
    
    chain.invoke({"foo": "bears"})  
    
    
    
        {'setup': "Why don't bears wear shoes?",  
         'punchline': 'Because they have bear feet!'}  
    
    
    
    from langchain.output_parsers.openai_functions import JsonKeyOutputFunctionsParser  
    chain = (  
        prompt   
        | model.bind(function_call= {"name": "joke"}, functions= functions)   
        | JsonKeyOutputFunctionsParser(key_name="setup")  
    )  
    

#### API Reference:

  * JsonKeyOutputFunctionsParser from `langchain.output_parsers.openai_functions`

    
    
    chain.invoke({"foo": "bears"})  
    
    
    
        "Why don't bears like fast food?"  
    

## Passthroughs and itemgetter​

Often times when constructing a chain you may want to pass along original
input variables to future steps in the chain. How exactly you do this depends
on what exactly the input is:

  * If the original input was a string, then you likely just want to pass along the string. This can be done with `RunnablePassthrough`. For an example of this, see `LLMChain + Retriever`
  * If the original input was a dictionary, then you likely want to pass along specific keys. This can be done with `itemgetter`. For an example of this see `Multiple LLM Chains`

    
    
    from langchain.schema.runnable import RunnablePassthrough  
    from operator import itemgetter  
    

#### API Reference:

  * RunnablePassthrough from `langchain.schema.runnable`

## LLMChain + Retriever​

Let's now look at adding in a retrieval step, which adds up to a "retrieval-
augmented generation" chain

    
    
    from langchain.vectorstores import Chroma  
    from langchain.embeddings import OpenAIEmbeddings  
    from langchain.schema.runnable import RunnablePassthrough  
    

#### API Reference:

  * Chroma from `langchain.vectorstores`
  * OpenAIEmbeddings from `langchain.embeddings`
  * RunnablePassthrough from `langchain.schema.runnable`

    
    
    # Create the retriever  
    vectorstore = Chroma.from_texts(["harrison worked at kensho"], embedding=OpenAIEmbeddings())  
    retriever = vectorstore.as_retriever()  
    
    
    
    template = """Answer the question based only on the following context:  
    {context}  
      
    Question: {question}  
    """  
    prompt = ChatPromptTemplate.from_template(template)  
    
    
    
    chain = (  
        {"context": retriever, "question": RunnablePassthrough()}   
        | prompt   
        | model   
        | StrOutputParser()  
    )  
    
    
    
    chain.invoke("where did harrison work?")  
    
    
    
        Number of requested results 4 is greater than number of elements in index 1, updating n_results = 1  
      
      
      
      
      
        'Harrison worked at Kensho.'  
    
    
    
    template = """Answer the question based only on the following context:  
    {context}  
      
    Question: {question}  
      
    Answer in the following language: {language}  
    """  
    prompt = ChatPromptTemplate.from_template(template)  
      
    chain = {  
        "context": itemgetter("question") | retriever,   
        "question": itemgetter("question"),   
        "language": itemgetter("language")  
    } | prompt | model | StrOutputParser()  
    
    
    
    chain.invoke({"question": "where did harrison work", "language": "italian"})  
    
    
    
        Number of requested results 4 is greater than number of elements in index 1, updating n_results = 1  
      
      
      
      
      
        'Harrison ha lavorato a Kensho.'  
    

## Multiple LLM Chains​

This can also be used to string together multiple LLMChains

    
    
    from operator import itemgetter  
      
    prompt1 = ChatPromptTemplate.from_template("what is the city {person} is from?")  
    prompt2 = ChatPromptTemplate.from_template("what country is the city {city} in? respond in {language}")  
      
    chain1 = prompt1 | model | StrOutputParser()  
      
    chain2 = {"city": chain1, "language": itemgetter("language")} | prompt2 | model | StrOutputParser()  
      
    chain2.invoke({"person": "obama", "language": "spanish"})  
    
    
    
        'El país en el que nació la ciudad de Honolulu, Hawái, donde nació Barack Obama, el 44º presidente de los Estados Unidos, es Estados Unidos.'  
    
    
    
    from langchain.schema.runnable import RunnableMap  
    prompt1 = ChatPromptTemplate.from_template("generate a random color")  
    prompt2 = ChatPromptTemplate.from_template("what is a fruit of color: {color}")  
    prompt3 = ChatPromptTemplate.from_template("what is countries flag that has the color: {color}")  
    prompt4 = ChatPromptTemplate.from_template("What is the color of {fruit} and {country}")  
    chain1 = prompt1 | model | StrOutputParser()  
    chain2 = RunnableMap(steps={"color": chain1}) | {  
        "fruit": prompt2 | model | StrOutputParser(),  
        "country": prompt3 | model | StrOutputParser(),  
    } | prompt4  
    

#### API Reference:

  * RunnableMap from `langchain.schema.runnable`

    
    
    chain2.invoke({})  
    
    
    
        ChatPromptValue(messages=[HumanMessage(content="What is the color of A fruit that has a color similar to #7E7DE6 is the Peruvian Apple Cactus (Cereus repandus). It is a tropical fruit with a vibrant purple or violet exterior. and The country's flag that has the color #7E7DE6 is North Macedonia.", additional_kwargs={}, example=False)])  
    

## Router​

You can also use the router runnable to conditionally route inputs to
different runnables.

    
    
    from langchain.chains import create_tagging_chain_pydantic  
    from pydantic import BaseModel, Field  
      
    class PromptToUse(BaseModel):  
        """Used to determine which prompt to use to answer the user's input."""  
          
        name: str = Field(description="Should be one of `math` or `english`")  
    

#### API Reference:

  * create_tagging_chain_pydantic from `langchain.chains`

    
    
    tagger = create_tagging_chain_pydantic(PromptToUse, ChatOpenAI(temperature=0))  
    
    
    
    chain1 = ChatPromptTemplate.from_template("You are a math genius. Answer the question: {question}") | ChatOpenAI()  
    chain2 = ChatPromptTemplate.from_template("You are an english major. Answer the question: {question}") | ChatOpenAI()  
    
    
    
    from langchain.schema.runnable import RouterRunnable  
    router = RouterRunnable({"math": chain1, "english": chain2})  
    

#### API Reference:

  * RouterRunnable from `langchain.schema.runnable`

    
    
    chain = {  
        "key": {"input": lambda x: x["question"]} | tagger | (lambda x: x['text'].name),  
        "input": {"question": lambda x: x["question"]}  
    } | router  
    
    
    
    chain.invoke({"question": "whats 2 + 2"})  
    
    
    
        AIMessage(content='Thank you for the compliment! The sum of 2 + 2 is equal to 4.', additional_kwargs={}, example=False)  
    

## Tools​

You can use any LangChain tool easily

    
    
    from langchain.tools import DuckDuckGoSearchRun  
    

#### API Reference:

  * DuckDuckGoSearchRun from `langchain.tools`

    
    
        /Users/harrisonchase/.pyenv/versions/3.9.1/envs/langchain/lib/python3.9/site-packages/deeplake/util/check_latest_version.py:32: UserWarning: A newer version of deeplake (3.6.14) is available. It's recommended that you update to the latest version using `pip install -U deeplake`.  
          warnings.warn(  
    
    
    
    search = DuckDuckGoSearchRun()  
    
    
    
    template = """turn the following user input into a search query for a search engine:  
      
    {input}"""  
    prompt = ChatPromptTemplate.from_template(template)  
    
    
    
    chain = prompt | model | StrOutputParser() | search  
    
    
    
    chain.invoke({"input": "I'd like to figure out what games are tonight"})  
    
    
    
        "What sports games are on TV today & tonight? Watch and stream live sports on TV today, tonight, tomorrow. Today's 2023 sports TV schedule includes football, basketball, baseball, hockey, motorsports, soccer and more. Watch on TV or stream online on ESPN, FOX, FS1, CBS, NBC, ABC, Peacock, Paramount+, fuboTV, local channels and many other networks. Weather Alerts Alerts Bar. Not all offers available in all states, please visit BetMGM for the latest promotions for your area. Must be 21+ to gamble, please wager responsibly. If you or someone ... Speak of the Devils. Good Morning Arizona. Happy Hour Spots. Jaime's Local Love. Surprise Squad. Silver Apple. Field Trip Friday. Seen on TV. Arizona Highways TV. MLB Games Tonight: How to Watch on TV, Streaming & Odds - Friday, July 28. San Diego Padres' Juan Soto plays during the first baseball game in a doubleheader, Saturday, July 15, 2023, in Philadelphia. (AP Photo/Matt Slocum) (APMedia) Today's MLB schedule features top teams in action. Among those games is the Texas Rangers playing the San Diego ... TV. Cleveland at Chi. White Sox. 1:10pm. Bally Sports. NBCS-CHI. Cleveland Guardians (50-51) are second place in AL Central and Chicago White Sox (41-61) are fourth place in AL Central. The Guardians are 23-27 on the road this season and White Sox are 21-26 at home. Chi. Cubs at St. Louis."  
    

## Arbitrary Functions​

You can use arbitrary functions in the pipeline

Note that all inputs to these functions need to be a SINGLE argument. If you
have a function that accepts multiple arguments, you should write a wrapper
that accepts a single input and unpacks it into multiple argument.

    
    
    from langchain.schema.runnable import RunnableLambda  
      
    def length_function(text):  
        return len(text)  
      
    def _multiple_length_function(text1, text2):  
        return len(text1) * len(text2)  
      
    def multiple_length_function(_dict):  
        return _multiple_length_function(_dict["text1"], _dict["text2"])  
      
    prompt = ChatPromptTemplate.from_template("what is {a} + {b}")  
      
    chain1 = prompt | model  
      
    chain = {  
        "a": itemgetter("foo") | RunnableLambda(length_function),  
        "b": {"text1": itemgetter("foo"), "text2": itemgetter("bar")} | RunnableLambda(multiple_length_function)  
    } | prompt | model  
    

#### API Reference:

  * RunnableLambda from `langchain.schema.runnable`

    
    
    chain.invoke({"foo": "bar", "bar": "gah"})  
    
    
    
        AIMessage(content='3 + 9 is equal to 12.', additional_kwargs={}, example=False)  
    

## SQL Database​

We can also try to replicate our SQLDatabaseChain using this style.

    
    
    template = """Based on the table schema below, write a SQL query that would answer the user's question:  
    {schema}  
      
    Question: {question}"""  
    prompt = ChatPromptTemplate.from_template(template)  
    
    
    
    from langchain.utilities import SQLDatabase  
    

#### API Reference:

  * SQLDatabase from `langchain.utilities`

    
    
    db = SQLDatabase.from_uri("sqlite:///../../../../notebooks/Chinook.db")  
    
    
    
    def get_schema(_):  
        return db.get_table_info()  
    
    
    
    def run_query(query):  
        return db.run(query)  
    
    
    
    inputs = {  
        "schema": RunnableLambda(get_schema),  
        "question": itemgetter("question")  
    }  
    sql_response = (  
            RunnableMap(inputs)  
            | prompt  
            | model.bind(stop=["\nSQLResult:"])  
            | StrOutputParser()  
        )  
    
    
    
    sql_response.invoke({"question": "How many employees are there?"})  
    
    
    
        'SELECT COUNT(*) \nFROM Employee;'  
    
    
    
    template = """Based on the table schema below, question, sql query, and sql response, write a natural language response:  
    {schema}  
      
    Question: {question}  
    SQL Query: {query}  
    SQL Response: {response}"""  
    prompt_response = ChatPromptTemplate.from_template(template)  
    
    
    
    full_chain = (  
        RunnableMap({  
            "question": itemgetter("question"),  
            "query": sql_response,  
        })   
        | {  
            "schema": RunnableLambda(get_schema),  
            "question": itemgetter("question"),  
            "query": itemgetter("query"),  
            "response": lambda x: db.run(x["query"])      
        }   
        | prompt_response   
        | model  
    )  
    
    
    
    full_chain.invoke({"question": "How many employees are there?"})  
    
    
    
        AIMessage(content='There are 8 employees.', additional_kwargs={}, example=False)  
    

## Code Writing​

    
    
    from langchain.utilities import PythonREPL  
    from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate  
    

#### API Reference:

  * PythonREPL from `langchain.utilities`
  * SystemMessagePromptTemplate from `langchain.prompts`
  * HumanMessagePromptTemplate from `langchain.prompts`

    
    
    template = """Write some python code to solve the user's problem.   
      
    Return only python code in Markdown format, eg:  
      
    ```python  
    ....  
    ```"""  
    prompt = ChatPromptTemplate(messages=[  
        SystemMessagePromptTemplate.from_template(template),  
        HumanMessagePromptTemplate.from_template("{input}")  
    ])  
    
    
    
    def _sanitize_output(text: str):  
        _, after = text.split("```python")  
        return after.split("```")[0]  
    
    
    
    chain = prompt | model | StrOutputParser() | _sanitize_output | PythonREPL().run  
    
    
    
    chain.invoke({"input": "whats 2 plus 2"})  
    
    
    
        Python REPL can execute arbitrary code. Use with caution.  
      
      
      
      
      
        '4\n'  
  
--- 

# Interface

In an effort to make it as easy as possible to create custom chains, we've
implemented a "Runnable" protocol that most components implement. This is a
standard interface with a few different methods, which makes it easy to define
custom chains as well as making it possible to invoke them in a standard way.
The standard interface exposed includes:

  * `stream`: stream back chunks of the response
  * `invoke`: call the chain on an input
  * `batch`: call the chain on a list of inputs

These also have corresponding async methods:

  * `astream`: stream back chunks of the response async
  * `ainvoke`: call the chain on an input async
  * `abatch`: call the chain on a list of inputs async

The type of the input varies by component. For a prompt it is a dictionary,
for a retriever it is a single string, for a model either a single string, a
list of chat messages, or a PromptValue.

The output type also varies by component. For an LLM it is a string, for a
ChatModel it's a ChatMessage, for a prompt it's a PromptValue, for a retriever
it's a list of documents.

Let's take a look at these methods! To do so, we'll create a super simple
PromptTemplate + ChatModel chain.

    
    
    from langchain.prompts import ChatPromptTemplate  
    from langchain.chat_models import ChatOpenAI  
    

#### API Reference:

  * ChatPromptTemplate from `langchain.prompts`
  * ChatOpenAI from `langchain.chat_models`

    
    
    model = ChatOpenAI()  
    
    
    
    prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")  
    
    
    
    chain = prompt | model  
    

## Stream​

    
    
    for s in chain.stream({"topic": "bears"}):  
        print(s.content, end="")  
    
    
    
        Sure, here's a bear-themed joke for you:  
          
        Why don't bears wear shoes?  
          
        Because they have bear feet!  
    

## Invoke​

    
    
    chain.invoke({"topic": "bears"})  
    
    
    
        AIMessage(content="Why don't bears wear shoes?\n\nBecause they already have bear feet!", additional_kwargs={}, example=False)  
    

## Batch​

    
    
    chain.batch([{"topic": "bears"}, {"topic": "cats"}])  
    
    
    
        [AIMessage(content="Why don't bears ever wear shoes?\n\nBecause they have bear feet!", additional_kwargs={}, example=False),  
         AIMessage(content="Why don't cats play poker in the wild?\n\nToo many cheetahs!", additional_kwargs={}, example=False)]  
    

## Async Stream​

    
    
    async for s in chain.astream({"topic": "bears"}):  
        print(s.content, end="")  
    
    
    
        Why don't bears wear shoes?  
          
        Because they have bear feet!  
    

## Async Invoke​

    
    
    await chain.ainvoke({"topic": "bears"})  
    
    
    
        AIMessage(content="Sure, here you go:\n\nWhy don't bears wear shoes?\n\nBecause they have bear feet!", additional_kwargs={}, example=False)  
    

## Async Batch​

    
    
    await chain.abatch([{"topic": "bears"}])  
    
    
    
        [AIMessage(content="Why don't bears wear shoes?\n\nBecause they have bear feet!", additional_kwargs={}, example=False)]  
        

---

 
## First part: general understanding

The LangChain Expression Language allows you to easily create chains of different components like prompts, models, retrievers, etc. This is a new type of way to contruct chains. There are two main benefits: a standard interface and easying piping.

### Standard Interface

All chains constructed this way will come with built in batch, async and streaming support.

### Easying piping

You can easily combine these chains together by using the `|` Operator

## Next: Creating a Simple Chain

### Import standard things

These are the same LangChain constructs we know

```python
from langchain.prompts import ChatPromptTemplate  
from langchain.chat_models import ChatOpenAI  
```

### Setup

Lets make a chain that takes in a topic and makes a joke.
We can do this by combining a PromptTemplate with a ChatModel.
Let's initialize those by themselves

```python
model = ChatOpenAI()  
prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")  
```

### Pipe

We can now chain those together with the `|` operator

```python
chain = prompt | model 
```

### Call

We can now call this with `.invoke`. We pass in a dictionary, because that's what PromptTemplate expects.

```python 
chain.invoke({"topic": "bears"})  
```

### Stream

Show code for this, explain why its useful

### Batch

Show code for this, explain why its useful

### Async

Show code for this, how to call async (only show `.ainvoke` but tell them it exists for `astream` and `abatch`)


## Output Parsers

The above chain returns a ChatMessage.
Often times it's more workable to work with strings.
We can use `StrOutputParser` to do that.
Check with them that this makes sense

### Show example of how to add in `StrOutputParser` and run

```python
from langchain.schema.output_parser import StrOutputParser  
chain = prompt | model | StrOutputParser()  
chain.invoke({"foo": "bears"})  
```

## More complicated chains

You can combine this knowledge over and over again to create more complicated chains.
Let's go over one final example - how to do retrieval QA.

### Set up the retriever

```python
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema.runnable import RunnablePassthrough

# Create the retriever
vectorstore = Chroma.from_texts(["harrison worked at kensho"], embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever()
```

### Set up the prompt template

```python
template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
```

### Create the chain

```python
chain = (
    {"context": retriever, "question": RunnablePassthrough()} 
    | prompt 
    | model 
    | StrOutputParser()
)
```

### Run the chain

Show code for this

## Conclusion

That's it! Excellent job. Check out https://python.langchain.com/docs/guides/expression_language/cookbook for more info.


    
