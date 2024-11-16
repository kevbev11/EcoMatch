import pandas as pd
import numpy as np
from openai import OpenAI
from typing import List, Dict, Tuple
import os
from sklearn.metrics.pairwise import cosine_similarity
import logging
from dotenv import load_dotenv
import users
load_dotenv()
class SemanticMatcher:
    def __init__(self, api_key: str = None, companies: List = None, organizations: List = None):
        """
        Initialize the SemanticMatcher with OpenAI API key, companies, and organizations.
        
        Args:
            api_key: OpenAI API key. If not provided, will look for OPENAI_API_KEY in environment variables.
            companies: List of Company instances.
            organizations: List of Organization instances.
        """
        if api_key is None:
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key is None:
                raise ValueError("OpenAI API key must be provided or set in OPENAI_API_KEY environment variable")
        
        self.client = OpenAI(api_key=api_key)
        self.embedding_cache = {}
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.companies = companies
        self.organizations = organizations

    def get_embedding(self, text: str) -> List[float]:
        """
        Get embedding for a text string using OpenAI's API.
        Implements caching to avoid redundant API calls.
        
        Args:
            text: Text to get embedding for
            
        Returns:
            List of embedding values
        """
        # Check cache first
        if text in self.embedding_cache:
            return self.embedding_cache[text]
        
        try:
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            embedding = response.data[0].embedding
            # Cache the result
            self.embedding_cache[text] = embedding
            return embedding
        except Exception as e:
            self.logger.error(f"Error getting embedding for text '{text}': {str(e)}")
            raise

    def find_matches(self, similarity_threshold: float = 0.00, max_matches: int = 3) -> List[Tuple[str, str, float]]:
        """
        Find semantic matches between supply (companies) and demand (organizations) items.

        Returns:
            List of tuples (company_name, organization_name, similarity_score).
        """
        supply_items = [(company.name, resource[0], resource[1], company.location) for company in self.companies for resource in company.resources]
        demand_items = [(organization.name, resource[0], resource[1], organization.location) for organization in self.organizations for resource in organization.resources]

        supply_embeddings = np.array([
            self.get_embedding(name) for _, name, _, _ in supply_items
        ])

        demand_embeddings = np.array([
            self.get_embedding(name) for _, name, _, _ in demand_items
        ])

        similarity_matrix = cosine_similarity(demand_embeddings, supply_embeddings)
        matches = []

        for i, demand in enumerate(demand_items):
            demand_org, demand_name, demand_quantity, demand_location = demand
            similarity_scores = similarity_matrix[i]
            top_indices = np.where(similarity_scores >= similarity_threshold)[0]
            top_indices = top_indices[np.argsort(similarity_scores[top_indices])[-max_matches:]]

            for idx in top_indices:
                supply_company = supply_items[idx][0]
                similarity_score = similarity_scores[idx]
                matches.append((supply_company, demand_org, similarity_score))

        # Sort matches by similarity score
        matches.sort(key=lambda x: x[2], reverse=True)
        return matches


if __name__ == "__main__":
    # Sample companies and organizations
    companies = [
        users.Company(name="Food Co", email="foodco@example.com", phone="123-456-7890",
                address="123 Food St, New York, NY", resources=["Canned tomato soup", "Whole grain pasta"], 
                quantity=[100, 150], time=2),
        users.Company(name="Baby Supplies Inc", email="baby@example.com", phone="987-654-3210",
                address="456 Baby Ave, Los Angeles, CA", resources=["Baby diapers size 4"], 
                quantity=[50], time=1)
    ]
    organizations = [
        users.Organization(name="Community Center", email="community@example.com", phone="222-333-4444",
                     address="202 Community Rd, New York, NY", resources=["Tomato soup", "Pasta noodles"], 
                     quantity=[80, 120], time=3),
        users.Organization(name="Child Care Home", email="childcare@example.com", phone="333-444-5555",
                     address="303 Childcare St, Los Angeles, CA", resources=["Diapers for infants"], 
                     quantity=[40], time=2)
    ]
    
    # Initialize matcher
    api_key = os.getenv("OPENAI_API_KEY")
    matcher = SemanticMatcher(api_key=api_key, companies=companies, organizations=organizations)
    
    # Find matches
    matches = matcher.find_matches()
    for match in matches:
        print(match)
