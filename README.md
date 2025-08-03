# 🦜 LangChain URL Summarizer

A Streamlit web application that automatically summarizes content from YouTube videos and websites using LangChain and Groq's Gemma model. Built with modern object-oriented programming principles for maintainability and extensibility.

## ✨ Features

- **Multi-Source Support**: Summarize content from YouTube videos and web pages
- **AI-Powered**: Uses Groq's Gemma-7b-It model for intelligent summarization
- **User-Friendly Interface**: Clean Streamlit web interface
- **Error Handling**: Comprehensive error handling and validation
- **Extensible Architecture**: Object-oriented design for easy feature additions
- **Secure**: API key input with password masking

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Groq API key (get one from [Groq Console](https://console.groq.com))

### Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run app.py
```

3. Open your browser and navigate to `http://localhost:8501`

## 📦 Dependencies

```
streamlit
langchain
langchain-groq
langchain-community
validators
```

Create a `requirements.txt` file with these dependencies:

```txt
streamlit>=1.28.0
langchain>=0.1.0
langchain-groq>=0.1.0
langchain-community>=0.0.13
validators>=0.22.0
```

## 🛠️ Usage

1. **Get your Groq API Key**:
   - Visit [Groq Console](https://console.groq.com)
   - Create an account and generate an API key

2. **Launch the Application**:
   - Run `streamlit run app.py`
   - The app will open in your default browser

3. **Enter Your API Key**:
   - In the sidebar, paste your Groq API key
   - The key is masked for security

4. **Add a URL**:
   - Enter a YouTube video URL or website URL
   - Supported formats:
     - `https://www.youtube.com/watch?v=VIDEO_ID`
     - `https://youtu.be/VIDEO_ID`
     - Any valid website URL

5. **Generate Summary**:
   - Click "🚀 Summarize the Content from YT or Website"
   - Wait for the AI to process and summarize the content
   - View your 300-word summary

## 🏗️ Architecture

The application follows object-oriented programming principles with a clean separation of concerns:

### Core Components

#### 1. **Abstract Document Loader (`DocumentLoader`)**
- Base class defining the interface for content loaders
- Ensures consistent behavior across different content types

#### 2. **Concrete Loaders**
- `YouTubeDocumentLoader`: Handles YouTube video transcription
- `WebsiteDocumentLoader`: Processes web page content

#### 3. **Factory Pattern (`DocumentLoaderFactory`)**
- Automatically selects the appropriate loader based on URL type
- Easily extensible for new content sources

#### 4. **Configuration Management (`SummarizerConfig`)**
- Centralizes application settings
- Easy to modify model parameters and prompts

#### 5. **Core Logic (`ContentSummarizer`)**
- Handles the main summarization workflow
- Integrates with LangChain and Groq API
- Provides comprehensive error handling

#### 6. **User Interface (`StreamlitUI`)**
- Manages all Streamlit-specific code
- Provides clean, intuitive user experience
- Handles user input validation

### Design Patterns Used

- **Abstract Factory Pattern**: For document loaders
- **Factory Pattern**: For loader selection
- **Single Responsibility Principle**: Each class has one clear purpose
- **Dependency Injection**: Configuration passed to components
- **Error Handling**: Centralized exception management

## 🔧 Configuration

### Model Settings

You can customize the summarization behavior by modifying the `SummarizerConfig` class:

```python
config = SummarizerConfig(
    model_name="Gemma-7b-It",  # Groq model to use
    max_words=300              # Summary length
)
```

### Supported Models

The application uses Groq's models. Popular options include:
- `Gemma-7b-It` (default)
- `llama2-70b-4096`
- `mixtral-8x7b-32768`

## 🛡️ Error Handling

The application includes comprehensive error handling for:

- **Invalid API Keys**: Clear error messages for authentication issues
- **Invalid URLs**: URL validation with helpful feedback
- **Network Issues**: Graceful handling of connection problems
- **Content Loading Errors**: Specific error messages for different failure types
- **Model Processing Errors**: Clear feedback when summarization fails

## 🔒 Security Features

- **API Key Protection**: Keys are masked in the UI and not stored
- **Input Validation**: All user inputs are validated before processing
- **SSL Configuration**: Proper SSL handling for web scraping
- **User Agent Headers**: Respectful web scraping practices

## 🚧 Extending the Application

### Adding New Content Sources

1. Create a new loader class inheriting from `DocumentLoader`:

```python
class PDFDocumentLoader(DocumentLoader):
    def load_documents(self, url: str) -> List:
        # Implementation for PDF loading
        pass
    
    def is_valid_url(self, url: str) -> bool:
        return url.endswith('.pdf')
```

2. Register it in `DocumentLoaderFactory`:

```python
def __init__(self):
    self.loaders = [
        YouTubeDocumentLoader(),
        WebsiteDocumentLoader(),
        PDFDocumentLoader()  # Add new loader
    ]
```

### Customizing the UI

The `StreamlitUI` class encapsulates all interface logic, making it easy to:
- Add new input fields
- Modify the layout
- Add new features like file uploads
- Integrate with other UI frameworks

### Adding New Models

Modify the `SummarizerConfig` class to support different AI providers:

```python
class SummarizerConfig:
    def __init__(self, provider="groq", model_name="Gemma-7b-It"):
        self.provider = provider
        self.model_name = model_name
        # Add provider-specific configurations
```

## 🐛 Troubleshooting

### Common Issues

1. **"Please provide a valid Groq API Key"**
   - Ensure your API key is correctly copied
   - Check that your Groq account has sufficient credits

2. **"Please enter a valid URL"**
   - Verify the URL is complete and accessible
   - Check for typos in the URL

3. **"Failed to load documents"**
   - The website might be blocking automated access
   - Try a different URL or check your internet connection

4. **"Failed to generate summary"**
   - The content might be too long or in an unsupported format
   - Try with a different piece of content

### Debug Mode

To enable detailed error logging, add this to your code:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Run linting
flake8 app.py

# Format code
black app.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) for the powerful LLM framework
- [Groq](https://groq.com/) for fast AI inference
- [Streamlit](https://streamlit.io/) for the beautiful web framework
- The open-source community for the various libraries used


