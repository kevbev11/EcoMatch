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

    def find_matches(self, 
                    similarity_threshold: float = 0.6,
                    max_matches: int = 3) -> List[Dict]:
        """
        Find semantic matches between supply (companies) and demand (organizations) items.
        
        Args:
            similarity_threshold: Minimum cosine similarity score to consider a match
            max_matches: Maximum number of matches to return for each demand item
            
        Returns:
            List of dictionaries containing matches and their details
        """
        # Prepare data for supply and demand items
        supply_items = [(company.name, resource[0], resource[1], company.location) for company in self.companies for resource in company.resources]
        demand_items = [(organization.name, resource[0], resource[1], organization.location) for organization in self.organizations for resource in organization.resources]
        
        # Get embeddings for all items
        supply_embeddings = np.array([
            self.get_embedding(name) for _, name, _, _ in supply_items
        ])
        
        demand_embeddings = np.array([
            self.get_embedding(name) for _, name, _, _ in demand_items
        ])
        
        # Calculate similarity matrix
        similarity_matrix = cosine_similarity(demand_embeddings, supply_embeddings)
        
        matches = []
        
        # Find matches for each demand item
        for i, demand in enumerate(demand_items):
            demand_org, demand_name, demand_quantity, demand_location = demand
            
            # Get similarity scores for this demand item
            similarity_scores = similarity_matrix[i]
            
            # Get indices of top matches above threshold
            top_indices = np.where(similarity_scores >= similarity_threshold)[0]
            top_indices = top_indices[np.argsort(similarity_scores[top_indices])[-max_matches:]]
            
            for idx in top_indices:
                supply_company, supply_name, supply_quantity, supply_location = supply_items[idx][0], supply_items[idx][1], supply_items[idx][2], supply_items[idx][3]
                similarity_score = similarity_scores[idx]
                
                matches.append({
                    'demand_organization': demand_org,
                    'demand_item': demand_name,
                    'demand_quantity': demand_quantity,
                    'supply_company': supply_company,
                    'supply_item': supply_name,
                    'supply_quantity': supply_quantity,
                    'similarity_score': similarity_score
                })
        
        # Sort matches by similarity score
        matches.sort(key=lambda x: x['similarity_score'], reverse=True)
        return matches

def example_usage():
    """Example usage of the SemanticMatcher class"""
    # Sample data for companies
    companies = [
        users.Company(name='Food Co', location='New York', resources=['Canned tomato soup', 'Whole grain pasta'], quantity=[100, 150], time=2),
        users.Company(name='Baby Supplies Inc', location='Los Angeles', resources=['Baby diapers size 4'], quantity=[50], time=1),
        users.Company(name='Soap Makers', location='Chicago', resources=['Antibacterial hand soap'], quantity=[200], time=3),
        users.Company(name='Warmth Ltd', location='San Francisco', resources=['Cotton blankets'], quantity=[30], time=5)
    ]
    
    # Sample data for organizations
    organizations = [
        users.Organization(name='Community Center', location='New York', resources=['Tomato soup', 'Pasta noodles'], quantity=[80, 120], time=3),
        users.Organization(name='Child Care Home', location='Los Angeles', resources=['Diapers for infants'], quantity=[40], time=2),
        users.Organization(name='Health Clinic', location='Chicago', resources=['Hand sanitizer'], quantity=[100], time=1),
        users.Organization(name='Shelter Home', location='San Francisco', resources=['Warm blankets'], quantity=[25], time=4)
    ]
    
    # Initialize matcher
    matcher = SemanticMatcher(companies=companies, organizations=organizations)
    
    # Find matches
    print("\nBasic Matches:")
    matches = matcher.find_matches()
    for match in matches:
        print(f"Demand: {match['demand_item']} ({match['demand_quantity']}) from {match['demand_organization']} -> "
              f"Supply: {match['supply_item']} ({match['supply_quantity']}) from {match['supply_company']} "
              f"[Similarity: {match['similarity_score']:.3f}]")

if __name__ == "__main__":
    example_usage()
