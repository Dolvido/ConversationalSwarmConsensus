import numpy as np
import openai

openai.api_key = "YOUR_API_KEY"

class Agent:
    def __init__(self, id):
        self.id = id
        self.opinion = None
    
    def make_decision(self, context, language_model):
        prompt = f"{context}\nAgent {self.id}, what is your decision?"
        self.opinion = language_model.generate_response(prompt)
    
    def update_opinion(self, context, opinions, language_model):
        prompt = f"{context}\nThe current opinions of the agents are:\n{opinions}\nAgent {self.id}, considering the opinions of other agents, what is your updated decision?"
        self.opinion = language_model.generate_response(prompt)

class LanguageModel:
    def __init__(self, engine):
        self.engine = engine
    
    def generate_response(self, prompt):
        response = openai.Completion.create(
            engine=self.engine,
            prompt=prompt,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.7,
        )
        
        return response.choices[0].text.strip()

class SwarmIntelligence:
    def __init__(self, num_agents, context, language_model):
        self.num_agents = num_agents
        self.context = context
        self.language_model = language_model
        self.agents = [Agent(i) for i in range(num_agents)]
    
    def initialize_opinions(self):
        for agent in self.agents:
            agent.make_decision(self.context, self.language_model)
    
    def update_opinions(self):
        opinions = "\n".join([f"Agent {agent.id}: {agent.opinion}" for agent in self.agents])
        for agent in self.agents:
            agent.update_opinion(self.context, opinions, self.language_model)
    
    def run_simulation(self, num_iterations):
        self.initialize_opinions()
        
        for _ in range(num_iterations):
            self.update_opinions()
        
        final_opinions = [agent.opinion for agent in self.agents]
        consensus_opinion = max(set(final_opinions), key=final_opinions.count)
        
        return consensus_opinion

# Example usage
context = "A company needs to decide on the best marketing strategy for their new product. The options are:\nA) Social media advertising\nB) Television commercials\nC) Print advertisements\nD) Influencer partnerships"
num_agents = 5
num_iterations = 3

language_model = LanguageModel("text-davinci-002")
swarm = SwarmIntelligence(num_agents, context, language_model)
consensus = swarm.run_simulation(num_iterations)

print(f"Collective Decision: {consensus}")