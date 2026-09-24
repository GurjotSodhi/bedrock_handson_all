---
title : "Memory + Runtime"
weight : 250
---

## AgentCore Runtime with AgentCore Memory

In the [Runtime: Deploy](../runtime-deploy) lab, we saw that conversation history is lost when a session ends. In this lab, we'll add AgentCore Memory to a deployed runtime so conversations persist across sessions and actor preferences carry over.

&nbsp;

## Setup

In the workshop environment's terminal, change directory to `runtime-memory`:

```bash
cd /environment/workshop/agentic-labs/runtime-memory
```

In the **runtime-memory** directory, review the following files:

- **math_tools.py** contains tool definitions
- **math_memory_agent.py** configures the agent with AgentCore Memory session manager and retrieval settings
- **math_memory_runtime.py** is the runtime entrypoint that accepts an actor ID in the request payload
- **create_memory_for_runtime.py** creates the AgentCore Memory resource
- **requirements.txt** lists dependencies for the deployed runtime

&nbsp;

## Create the memory


Run the following command to create the memory:

```bash
python create_memory_for_runtime.py
```

After a few minutes, this will display the ID for the created memory.

&nbsp;

## Create the runtime

Configure runtime:

```bash
agentcore configure --entrypoint math_memory_runtime.py
```

Accept the defaults until you reach the **Memory Configuration** step.

At the Memory Configuration step, select the number for the resource that starts with `DemoAgentRuntimeMemory-`.

Next, deploy the runtime:

```bash
agentcore deploy
```

When you specified the memory during the setup process, that memory's ID gets saved to a runtime environment variable named **BEDROCK_AGENTCORE_MEMORY_ID**.  You can see the runtime's environment variables in the Console for the specific Runtime's version, under **Advanced configurations**.


&nbsp;

### Test the Runtime


First we need to create a unique actor ID and Session ID:


```bash
export DEMO_ACTOR_ID=$(uuidgen)
echo DEMO_ACTOR_ID: $DEMO_ACTOR_ID

export DEMO_SESSION_ID=$(uuidgen)
echo DEMO_SESSION_ID: $DEMO_SESSION_ID
```

Note: In this example, we pass the actor ID in the request payload, trusting the caller to identify the actor. In a production system with sensitive user data, you'll want to use an auth scheme that verifies the actor's identity.

* [Commentary on Actor ID and Session Management](https://github.com/awslabs/agentcore-samples/blob/main/06-workshops/04-AgentCore-memory/03-advanced-patterns/02-memory-runtime-integration/runtime_memory_integration.ipynb)
* [Using inbound auth with AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-oauth.html)
* [Learn more about AgentCore Identity](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html)


&nbsp;

Now we can test calling the runtime, and feed in some of our facts and preferences:

```bash
agentcore invoke '{"prompt":"I like cats. My favorite color is green. Please respond to me using rhymes.", "actor_id":"'"$DEMO_ACTOR_ID"'"}' --session-id $DEMO_SESSION_ID
```

This should generate a response like this:

```json
{
    "result": 
        "How delightful to meet you today,
        A cat lover, I'd venture to say!
        With green as your hue,
        So fresh as the dew,
        You've brightened my circuits this way!

        Your feline friends purr 
        and they play,
        In meadows of green, bright and gay.
        With emerald eyes gleaming,
        And soft fur so seeming,
        They lounge in the grass where they lay!

        Is there something you'd like me to do?
        A calculation or task just for you?
        I'm here to assist,
        Whatever you've missed,
        Just ask and I'll see it right through!",
    "session_id": "d4550461-7cdf-4371-804a-93fb3f849bb5"
}

```

We can add some more preferences:

```bash
agentcore invoke '{"prompt":"Please use emojis when responding.", "actor_id":"'"$DEMO_ACTOR_ID"'"}' --session-id $DEMO_SESSION_ID
```


Then we can chat for a bit:

```bash
agentcore invoke '{"prompt":"Why are sunsets colorful?", "actor_id":"'"$DEMO_ACTOR_ID"'"}' --session-id $DEMO_SESSION_ID
```

Then confirm the agent is retaining this conversation:

```bash
agentcore invoke '{"prompt":"What have we discussed so far?", "actor_id":"'"$DEMO_ACTOR_ID"'"}' --session-id $DEMO_SESSION_ID
```

This should generate a response like this:

```json
{
    "result":
        "Let me recall our chat with care! 💭
        The topics that we came to share 📝
        First, you told me true 💚
        That green's the color for you 🌿
        And cats 🐱 are creatures beyond compare! 😻
        You asked me then to rhyme my speech 🎵
        So poetry would be my reach 📜
        With rhythm and with verse 🎭
        I'd answer and converse 💬
        Making every line a lyrical teach! ✨
        Then emojis joined the fun! 🎉
        To brighten every word and pun 😄
        With symbols bright and clear 💫
        To bring you extra cheer 🌟
        Adding flair to all that I had done! 🎨
        And sunsets colorful you asked about 🌅
        Why colors change without a doubt 🤔
        Through scattering of light 💡
        From blue to red so bright ❤️🧡
        That's what our discussion was about! 🌈
        So cats 🐱, green 💚, rhymes 🎵, and sky 🌄
        Are all the things we've covered, my! 👏
        Is there something more 🤷
        You'd like to explore? 🔍
        Just ask and I will surely try! 💪",
    "session_id": "d4550461-7cdf-4371-804a-93fb3f849bb5"
}
```

&nbsp;

### Stopping and resuming a session

The runtime session lives until its idle timeout is hit (default: 900 seconds / 15 minutes). In the [Runtime: Deploy](../runtime-deploy) lab, stopping a session meant losing the conversation entirely. With Memory connected, the session's conversation can be resumed.

Stop the session to end the running agent:

```bash
agentcore stop-session --session-id $DEMO_SESSION_ID
```

Invoke the agent again with the same actor ID and session ID:

```bash
agentcore invoke '{"prompt":"What have we discussed so far?", "actor_id":"'"$DEMO_ACTOR_ID"'"}' --session-id $DEMO_SESSION_ID
```

This should generate a response like this, where the specific conversation is recalled, including the question about sunsets:

```json
{
    "result": 
        "Let me recap what we've been through! 🔄
        All the topics, me and you 👥

        You love cats 🐱 so very much 😻
        And green 💚 is your favorite touch 🌿
        These preferences you shared 
        with glee! ✨

        Then rhymes 🎵 you asked me to compose 📝
        In poetic style, as language flows 🌊
        With rhythm in each line 📜
        To make the words align 💫
        Like verses and like rhythmic prose! 🎭

        Next, emojis 😊 you wanted too 🎨
        To add some color 🌈 to our view 👀
        With symbols bright and fun 🎉
        Beside each word I'd spun 💬
        To make responses pop for you! ✨

        Then sunset questions 🌅 came along 🤔
        Why colors paint the sky so strong 🎨
        I explained the light 💡
        Scatters blue from sight 💙
        While red and orange 🧡❤️ sing their song! 🌄

        And now you've asked me 
        twice to say 2️⃣
        What we discussed along the way 🛤️
        So here's the recap told 📋
        Our conversation bold 💪
        That's everything up to today! 📅",
    "session_id": "d4550461-7cdf-4371-804a-93fb3f849bb5"
}
```

Recall in the [Runtime: Deploy](../runtime-deploy#what-happens-when-a-session-ends) lab, the conversation would start over from scratch after the session was ended.

&nbsp;

### Starting a new session with the same actor

Now let's start a new session without changing the actor ID.

```bash
export DEMO_SESSION_ID=$(uuidgen)
echo DEMO_SESSION_ID: $DEMO_SESSION_ID
```

```bash
agentcore invoke '{"prompt":"What have we discussed so far?", "actor_id":"'"$DEMO_ACTOR_ID"'"}' --session-id $DEMO_SESSION_ID
```

We can see that preferences are pulled in from AgentCore Memory, but this is a new conversation with the same actor:

```json
{
    "result":
        "We haven't discussed anything yet! 🌟 
        This is the first message you've sent to me in this conversation.
        Our chat is fresh and new, you see! ✨

        However, I can see from context 
        that you have some preferences, it's true - 
        You like when I rhyme and use emojis too! 😊💚
        Your favorite color is green, so bright and clean 💚🍀
        And cats are creatures you think are keen! 
        🐱😺

        So now our discussion has just begun today,
        Feel free to ask me anything - I'm here to help in every way! 🎉",
    "session_id": "1a259325-1e62-43d8-be92-59a7677bb709"
}
```

&nbsp;

### Starting a new session with a different actor

Finally, create a new actor and session:

```bash
export DEMO_ACTOR_ID=$(uuidgen)
echo DEMO_ACTOR_ID: $DEMO_ACTOR_ID

export DEMO_SESSION_ID=$(uuidgen)
echo DEMO_SESSION_ID: $DEMO_SESSION_ID
```

```bash
agentcore invoke '{"prompt":"What have we discussed so far?", "actor_id":"'"$DEMO_ACTOR_ID"'"}' --session-id $DEMO_SESSION_ID
```

Generates a response like this:

```json
{
    "result":
        "We haven't discussed anything yet! This is the beginning of our conversation. I'm here to help you with calculations involving sine, cosine, and division operations.
        Is there something you'd like to calculate or discuss?",
    "session_id": "ac8d9d8e-b445-4d7b-b2ae-53e5b788674d"
}
```

A new actor has no memory history, so the agent starts fresh with no preferences or context.

&nbsp;

## Next

In the next section, we'll use the Model Context Protocol (MCP) to connect agents to external tools.
