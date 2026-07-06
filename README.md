AI Smart Bug Analyzer & Fix Advisor – Phase 1 Lecture
🌟 Introduction

Good morning/afternoon everyone.

Today, I am going to explain the first phase of our project "AI Smart Bug Analyzer & Fix Advisor."

Before we start, let me ask you a simple question.

Have you ever worked on a software project where the same bug keeps appearing again and again?

Imagine you're a software developer. One day, a user reports:

"The application crashes when I click the Save button."

You spend two hours finding the problem and fixing it.

A few weeks later, another user reports:

"The application closes after pressing Save."

Although the wording is different, it's actually the same issue. Without a proper system, another developer may spend two more hours solving the same problem again.

This is exactly the problem our project aims to solve.

The long-term goal is to build an AI system that can search previous bug reports and suggest possible solutions. However, before AI can do that, we first need a strong foundation. That foundation is what we completed in Phase 1.

📌 Task 1 – Understanding the Core Concepts

The first task was to understand the concepts that our future AI system will use.

The first concept is workflow.

A workflow is simply the sequence of steps that data follows inside a system.

Think about ordering food online. You place an order, the restaurant receives it, the chef prepares the food, the delivery partner picks it up, and finally it reaches you. This is a workflow because each step happens in a specific order.

Our project follows a similar process. A user submits a bug report, the system validates the information, cleans the data, stores it in a knowledge base, and later the AI will analyze it.

The next concept is Retrieval-Augmented Generation (RAG).

Normally, when we ask an AI a question, it answers using the knowledge it has already learned. With RAG, the AI first searches a collection of previous documents, retrieves the most relevant ones, and then uses those documents to generate a better answer.

For our project, this means that before suggesting a fix, the AI will first search previous bug reports to see if a similar issue has already been solved.

Another important concept is embeddings.

Computers cannot understand language the way humans do. They work with numbers. An embedding converts a sentence into a list of numbers that represents its meaning.

For example, the sentence "Application crashes while saving" is converted into a mathematical vector. This allows the computer to compare meanings instead of just comparing words.

Finally, we studied similarity search.

Suppose our database contains two bug reports:

"Application crashes after clicking Save."
"Dark mode is not working."

If a new bug says "App closes while saving," similarity search identifies that it is related to the first bug because the meanings are similar, even though the exact words are different.

🏗️ Task 2 – Designing the System Architecture

Once we understood the concepts, the next step was designing the architecture.

Architecture is the blueprint of the entire system. Just as a building needs an architectural plan before construction begins, software also requires a design before development.

Our architecture starts with the user. The user enters a bug description or uploads a log file through the Bug Submission Module.

The submitted information is passed to the Preprocessing Agent, which cleans and formats the text.

The cleaned data is then stored in the Knowledge Base.

Although the AI modules are not implemented yet, the architecture already reserves space for future components such as the Embedding Agent, Retrieval Agent, and Fix Advisor Agent.

Designing the architecture first helps ensure that the project is modular, scalable, and easy to maintain.

🤖 Task 3 – Defining the Five AI Agents

Instead of creating one large program to handle everything, we divided the project into five specialized agents.

This is similar to how different employees in a company perform different jobs.

The first is the Submission Agent. Its responsibility is to accept bug descriptions, upload log files, validate the input, and generate a unique Bug ID.

The second is the Preprocessing Agent. This agent cleans the data by converting text to lowercase, removing unnecessary symbols, eliminating extra spaces, and preparing the bug report for future AI processing.

The third is the Embedding Agent. Although it is not implemented yet, its future responsibility is to convert bug descriptions into numerical vectors called embeddings.

The fourth is the Retrieval Agent. This agent will search the vector database and retrieve bug reports that are semantically similar to the new bug.

Finally, the Fix Advisor Agent will analyze the retrieved bug reports and generate possible solutions, root causes, and recommendations.

By separating responsibilities among different agents, the system becomes easier to update, test, and expand.

🗄️ Task 4 – Designing the Knowledge Base

The next task was to design the knowledge base.

A knowledge base is simply an organized storage system for bug information.

Instead of storing random text files, we decided that every bug report should have a standard structure.

Each bug includes fields such as:

Bug ID
Title
Description
Module
Priority
Severity
Programming Language
Operating System
Stack Trace
Expected Behaviour
Actual Behaviour
Suggested Fix
Status

Having a structured knowledge base is extremely important because AI systems work much better with organized and consistent data.

At this stage, we are storing the information in CSV format. In the next phase, this knowledge base will be migrated to a vector database.

💻 Task 5 – Developing the Bug Submission Module

The final completed task was building the Bug Submission Module.

This module provides the interface through which users interact with the system.

The user can type a bug description into a text area or upload a log file.

The system validates the input to make sure the required information is provided.

Once the user clicks the Submit button, a unique Bug ID is generated, a timestamp is recorded, and the information is stored in the knowledge base.

The module also displays success messages and handles invalid input gracefully.

Although this module appears simple, it forms the entry point for the entire AI pipeline that will be implemented in future phases.

🎯 What We Have Achieved

By completing these five tasks, we have successfully built the foundation of the project.

We now have:

A clear understanding of the workflow and AI concepts.
A well-designed system architecture.
Clearly defined responsibilities for each AI agent.
A structured knowledge base design.
A functional Bug Submission Module.

This foundation ensures that the next phase of development can focus entirely on implementing AI features without redesigning the system.

🚀 Future Scope

In the next phase, we plan to implement advanced AI capabilities, including:

Generating text embeddings.
Using a vector database such as ChromaDB.
Performing semantic similarity search.
Implementing Retrieval-Augmented Generation (RAG).
Integrating a Large Language Model to recommend bug fixes.

These features will transform the current system into a complete AI-powered Bug Analyzer and Fix Advisor.

🎤 Conclusion

To conclude, this first phase was focused on building a solid and scalable foundation rather than implementing AI directly.

By understanding the workflow, designing the architecture, defining specialized agents, organizing the knowledge base, and developing the Bug Submission Module, we have prepared the system for future AI integration.

Thank you for your attention.
