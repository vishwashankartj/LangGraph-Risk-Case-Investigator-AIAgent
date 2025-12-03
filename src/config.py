"""
Configuration management for the High-Risk Investigation Agent.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration."""
    
    # LLM Provider
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "google").lower()  # "openai" or "google"
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    
    # LLM Model Configuration
    LLM_MODEL = os.getenv("LLM_MODEL", "gemini-pro")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    
    # Risk Score Thresholds
    RISK_THRESHOLD_LOW = int(os.getenv("RISK_THRESHOLD_LOW", "25"))
    RISK_THRESHOLD_MEDIUM = int(os.getenv("RISK_THRESHOLD_MEDIUM", "50"))
    RISK_THRESHOLD_HIGH = int(os.getenv("RISK_THRESHOLD_HIGH", "75"))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Risk Actions Mapping
    RISK_ACTIONS = {
        "low": "Approve",
        "medium": "Monitor",
        "high": "Soft-ban",
        "critical": "Full Account Suspension"
    }
    
    @classmethod
    def get_llm(cls):
        """Get configured LLM instance."""
        if cls.LLM_PROVIDER == "google":
            from langchain_google_genai import ChatGoogleGenerativeAI
            return ChatGoogleGenerativeAI(
                model=cls.LLM_MODEL,
                temperature=cls.LLM_TEMPERATURE,
                google_api_key=cls.GOOGLE_API_KEY
            )
        else:  # openai
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                model=cls.LLM_MODEL,
                temperature=cls.LLM_TEMPERATURE,
                api_key=cls.OPENAI_API_KEY
            )
    
    @classmethod
    def has_api_key(cls) -> bool:
        """Check if API key is configured for the selected provider."""
        if cls.LLM_PROVIDER == "google":
            return bool(cls.GOOGLE_API_KEY)
        else:
            return bool(cls.OPENAI_API_KEY)
    
    @classmethod
    def get_risk_level(cls, score: float) -> str:
        """Get risk level based on score."""
        if score <= cls.RISK_THRESHOLD_LOW:
            return "low"
        elif score <= cls.RISK_THRESHOLD_MEDIUM:
            return "medium"
        elif score <= cls.RISK_THRESHOLD_HIGH:
            return "high"
        else:
            return "critical"
    
    @classmethod
    def get_recommended_action(cls, score: float) -> str:
        """Get recommended action based on risk score."""
        risk_level = cls.get_risk_level(score)
        return cls.RISK_ACTIONS[risk_level]
