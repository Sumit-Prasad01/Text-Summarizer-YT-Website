import validators
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader
from abc import ABC, abstractmethod
from typing import List, Optional
import logging


class DocumentLoader(ABC):
    """Abstract base class for document loaders"""

    @abstractmethod
    def load_documents(self, url: str) -> List:
        """Load documents from the given url"""
        pass

    @abstractmethod
    def is_valid_url(self, url: str) -> bool:
        """Check if the URL is valid for this loader"""
        pass

class YouTubeDocumentLoader(DocumentLoader):
    """Concrete implementation for loading YouTube videos"""

    def load_documents(self, url: str) -> List:
        """Load documents from YouTube URL"""
        loader = YoutubeLoader.from_youtube_url(url, add_video_info = True)
        return loader.load()
    
    def is_valid_url(self, url: str) -> bool:
        """Check if URL is a YouTube URL"""
        return "youtube.com" in url or "youtu.be" in url
    
class WebsiteDocumentLoader(DocumentLoader):
    """Concrete implementation for loading website content"""
    def __init__(self):
       self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
        }
       
    def load_documents(self, url: str) -> List:
        """Load documents from website URL"""
        loader = UnstructuredURLLoader(
            urls=[url],
            ssl_verify = False,
            headers = self.headers
        )
        return loader.load()
    
    def is_valid_url(self, url: str) -> bool:
        """Check if URL is a valid website URL"""
        return validators.url(url) and "youtube.com" not in url and "youtu.be" not in url 
    

class DocumentLoaderFactory:
    """Factory class to create appropriate document loaders"""

    def __init__(self):
        self.loaders = [
            YouTubeDocumentLoader(),
            WebsiteDocumentLoader()
        ]
    
    def get_loader(self, url: str) -> Optional[DocumentLoader]:
        """Get the appropriate loader for the given url"""
        for loader in self.loaders:
            if loader.is_valid_url(url):
                return loader
            
        return None
    
class SummarizerConfig:
    """Configuration class for the summarizer"""

    def __init__(self, model_name: str = "Gemma-7b-It", max_words: int = 300):
        self.model_name = model_name
        self.max_words = max_words
        self.prompt_template = f"""
        Provide a summary of the following content in {max_words} words:
        Content:{{text}}
        """

        
class ContentSummarizer:
    """Main class for content summarization"""

    def __init__(self, config: SummarizerConfig):
        self.config = config
        self.loader_factory = DocumentLoaderFactory()
        self.llm = None
        self.prompt = PromptTemplate(
            template=self.config.prompt_template,
            input_variables=["text"]
        )

    def initialize_llm(self, groq_api_key : str) -> bool:
        """Initialize the language model with API key"""
        try:
            self.llm = ChatGroq(
                model = self.config.model_name,
                groq_api_key = groq_api_key
            )
            return True
        except Exception as e:
            logging.error(f"Failed to initialized LLM: {e}")
            return False
        
    def validate_inputs(self, groq_api_key : str, url : str) -> tuple[bool, str]:
        """validate the input parameters"""
        if not groq_api_key.strip():
            return False, "Please provide a valid API Key"
        
        if not url.strip():
            return False, "Please provide a URL"

        if not validators.url(url):
            return False, "Please enter a valid URL. It can be a Youtube URL or a Website URL."
        
        return True, ""
    
    def load_documents(self, url : str) -> tuple[Optional[List], str]:
        """Load documents from the given URL"""
        try:
            loader = self.loader_factory.get_loader(url)
            if not loader:
                return None, "Unsupported URL format"
            
            documents = loader.load_documents(url)
            return documents, ""
        
        except Exception as e:
            return None, f"Failed to load documents : {str(e)}"
        

    def summarize_content(self, documents : List) -> tuple[Optional[str], str]:
        """Summarize the loaded documents"""
        try: 
            if not self.llm:
                return None, "Language model not initialized"
            
            chain = load_summarize_chain(
                self.llm,
                chain_type = 'stuff',
                prompt = self.prompt
            )
            summary = chain.run(documents)
            return summary, ""
    
        except Exception as e:
            return None, f"Failed to generate summary: {str(e)}"
        
    def process_url(self, groq_api_key : str, url : str) -> tuple[Optional[str], str]:
        """Main method to process URL and return summary"""

        is_valid, error_msg = self.validate_inputs(groq_api_key, url)
        if not is_valid:
            return None, error_msg
        
        if not self.initialize_llm(groq_api_key):
            return None, "Failed to initialize language model"
        
        documents, error_msg = self.load_documents(url)
        return None, error_msg
    
        summary, error_msg = self.summarize_content(documents)
        if summary is None:
            return None, error_msg
        
        return summary, ""
    

class StreamlitUI:
    """Class to handle Streamlit user interface"""

    def __init__(self):
        self.summarizer = ContentSummarizer(SummarizerConfig())
        self.setup_page_config()


    def setup_page_config(self):
        """Setup Streamlit page configuration"""
        st.set_page_config(
            page_title="LangChain: Summarize Text From YT or Website",
            page_icon="🦜"
        )

    def render_header(self):
        """Render the page header"""
        st.title("🦜 LangChain: Summarize Text From YT or Website")
        st.subheader('Summarize URL')

    def render_sidebar(self) -> str:
        """Render sidebar and return API key"""
        with st.sidebar:
            groq_api_key = st.text_input(
                "Groq API Key",
                value = "",
                type = 'password',
                help = "Enter your Groq API key to use the summarization service"
            )
        return groq_api_key
    
    def render_main_content(self) -> str:
        """Render main content area and return URL"""
        url = st.text_input(
            "URL",
            label_visibility = "collapsed",
            placeholder = "Enter YouTube video URL website URL here...."
        )
        return url
    
    def handel_summarization(self, groq_api_key : str, url : str):
        """Handle the summarization process"""
        with st.spinner("Processing... Please wait while we analyze the content."):
            summary, error_msg = self.summarizer.process_url(groq_api_key, url)

            if summary:
                st.success("✅ Summary generated successfully!")
                st.write("### Summary")
                st.write(summary)

            else:
                st.error(f"❌ Error: {error_msg}")

    def run(self):
        """Main method to run the Streamlit application"""
        self.render_header()

        groq_api_key = self.render_sidebar()
        url = self.render_main_content()

        if st.button("🚀 Summarize the Content from YT or Website"):
            self.handel_summarization(groq_api_key, url)

def main():
    """Main function to run the application"""
    try:
        app = StreamlitUI()
        app.run()

    except Exception as e:
        st.error(f"Application error : {str(e)}")
        logging.error(f"Application error : {e}")


if __name__ == "__main__":
    main()