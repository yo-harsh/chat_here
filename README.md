# Chat_Here</>

Welcome to the README for the Chat_Here</> which is a Wildlife Guide Chatbot and PDF Analyzer, a Django project that provides information about wildlife and allows users to analyze PDF documents with AI-powered features. This project was built using the Lang-Chain and OpenAI libraries.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

The Wildlife Guide Chatbot and PDF Analyzer is a web application that combines the power of language models and document analysis to provide two main functionalities:

1. **Wildlife Guide Chatbot**: Users can interact with a chatbot that provides information about various animals. Simply ask a question about an animal, and the chatbot will provide detailed information about it.

2. **PDF Analyzer**: Users can upload PDF documents and ask questions about the content. The application uses AI to extract and analyze text from the PDF, making it easy to get answers to specific questions related to the document.

## Features

- Wildlife Guide Chatbot with OpenAI integration.
- PDF Analyzer with Lang-Chain integration for document processing.
- User-friendly web interface for both chatbot and PDF analyzer.
- Python 3.8+ and Django 4.2.5 compatibility.

## Installation

Follow these steps to set up and run the project on your local machine:

1. Clone the repository:

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

1. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use: venv\Scripts\activate
    ```

2. **Install the project dependencies from the `requirements.txt` file:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Migrate the database and create a superuser for the Django admin panel:**

    ```bash
    python manage.py migrate
    python manage.py createsuperuser
    ```

2. **Start the Django development server:**

    ```bash
    python manage.py runserver
    ```

3. **Access the web application by opening a web browser and navigating to [http://127.0.0.1:8000/](http://127.0.0.1:8000/). You can use the Wildlife Guide Chatbot and PDF Analyzer via the user interface.**

## Dependencies

The project relies on several Python libraries, and you can find them listed in the `requirements.txt` file. Here are some of the key dependencies:

- `dataclasses-json` for data serialization and deserialization.
- `Django` as the web framework.
- `openai` for integrating with the OpenAI language model.
- `langchain` for document processing and analysis.
- Others for various utilities and functionality.

## Contributing

1. **Fork the repository.**
2. **Create a new branch for your feature or fix.**
3. **Make your changes.**
4. **Create a pull request with a clear description of your changes.**

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute it as you see fit.

Enjoy using the Wildlife Guide Chatbot and PDF Analyzer! If you have any questions or encounter issues, please feel free to reach out or open an issue on the GitHub repository.
