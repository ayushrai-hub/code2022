import numpy as np
from typing import List, Dict, Any

class MainRecommender(BaseModel):
    user_selection: UserSelection
    history_manager: HistoryLogger
    
    def give_recommendation_dfs(self):
        raise NotImplementedError("This method should be implemented by subclasses.")
    
    def give_recommendation_bfs(self):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def standardize_probabilities(self, probs) -> List[float]:
        """Normalize probabilities to sum to 1"""
        if not probs:
            print("No probabilities provided, cannot sample.")
            return []
        
        total_prob = sum(probs)
        if total_prob == 0:
            print("Total probability for the group is zero, cannot sample.")
            return []
        return [prob / total_prob for prob in probs]

    def get_label_for_prompt(self, prompt: str) -> str:
        """Helper method to get label for a given prompt"""
        df = self.history_manager.prompts_manager.df_prompts
        return df[df['prompts'] == prompt]['labels'].iloc[0]

    def sample_and_update(self, possible_prompts: List[str], probs: List[float], 
                         num_samples: int, params: List[Any], mode: str = 'recommendations') -> List[str]:
        """Common method to sample prompts and update history manager"""
        if not possible_prompts:
            print("No possible prompts found.")
            return []
        
        standardized_probs = self.standardize_probabilities(probs)
        if not standardized_probs:
            return []
        
        # Ensure we don't sample more than available
        num_samples = min(num_samples, len(possible_prompts))
        
        recommended_prompts = np.random.choice(
            possible_prompts, 
            size=num_samples, 
            replace=False, 
            p=standardized_probs
        )
        
        self.history_manager.update_prompt_probabilities(
            recommended_prompts, 
            params=params, 
            mode=mode
        )
        
        return recommended_prompts.tolist()


class NoParamsRecommendation(MainRecommender):
    
    def _get_same_label_prompts(self, label: str) -> List[str]:
        """Get prompts with same label and no parameters"""
        df = self.history_manager.prompts_manager.df_prompts
        return df[(df['labels'] == label) & (df['params'].apply(lambda x: len(x) == 0))]['prompts'].tolist()
    
    def _get_probabilities_for_prompts(self, prompts: List[str]) -> List[float]:
        """Get no_params probabilities for given prompts"""
        return [self.history_manager.prompt_probabilities['no_params'][prompt] for prompt in prompts]

    def give_recommendation_dfs(self):
        """Deep dive recommendation: same label, no parameters"""
        prompt = self.user_selection.prompt
        label = self.get_label_for_prompt(prompt)
        
        possible_prompts = self._get_same_label_prompts(label)
        probs = self._get_probabilities_for_prompts(possible_prompts)
        
        return self.sample_and_update(
            possible_prompts, 
            probs, 
            self.user_selection.numDeepDive,
            [None] * self.user_selection.numDeepDive
        )

    def give_recommendation_bfs(self):
        """Broad exploration: closest cluster, no parameters"""
        prompt = self.user_selection.prompt
        label = self.get_label_for_prompt(prompt)
        
        # Find closest cluster
        relevant_distances = {
            pair: dist for pair, dist in self.history_manager.prompts_manager.cluster_distances.items() 
            if label in pair
        }
        
        if not relevant_distances:
            print(f"No cluster distances found for label: {label}")
            return []
        
        min_distance = min(relevant_distances.values())
        closest_pair = next(pair for pair, dist in relevant_distances.items() if dist == min_distance)
        closest_cluster_label = closest_pair.replace(label + ',', '').replace(',' + label, '')
        
        possible_prompts = self._get_same_label_prompts(closest_cluster_label)
        probs = self._get_probabilities_for_prompts(possible_prompts)
        
        return self.sample_and_update(
            possible_prompts, 
            probs, 
            self.user_selection.numExploration,
            [None] * self.user_selection.numExploration
        )


class ParamRecommendation(MainRecommender):
    
    def _get_key_param_for_prompt(self, prompt: str) -> str:
        """Get the first parameter for a given prompt"""
        df = self.history_manager.prompts_manager.df_prompts
        return df[df['prompts'] == prompt]['params'].str[0].iloc[0]
    
    def _get_prompts_with_param(self, key_param: str) -> List[str]:
        """Get prompts that have exactly the specified parameter"""
        df = self.history_manager.prompts_manager.df_prompts
        return df[df['params'].apply(lambda x: str(x) == str([key_param]))]['prompts'].tolist()
    
    def _ensure_param_value_exists(self, prompts: List[str], key_param: str, key_param_value: Any):
        """Ensure parameter value exists in prompt probabilities"""
        for prompt in prompts:
            if key_param_value not in self.history_manager.prompt_probabilities['params'][prompt][key_param]:
                self.history_manager.prompt_probabilities['params'][prompt][key_param][key_param_value] = 1

    def give_recommendation_dfs(self):
        """Deep dive recommendation: same parameter type and value"""
        prompt = self.user_selection.prompt
        key_param = self._get_key_param_for_prompt(prompt)
        key_param_value = self.user_selection.parameters[key_param]
        
        possible_prompts = self._get_prompts_with_param(key_param)
        self._ensure_param_value_exists(possible_prompts, key_param, key_param_value)
        
        probs = [
            self.history_manager.prompt_probabilities['params'][prompt][key_param][key_param_value] 
            for prompt in possible_prompts
        ]
        
        return self.sample_and_update(
            possible_prompts, 
            probs, 
            self.user_selection.numDeepDive,
            [{key_param: key_param_value}] * self.user_selection.numDeepDive
        )

    def give_recommendation_bfs(self):
        """Broad exploration: same label, no parameters"""
        prompt = self.user_selection.prompt
        label = self.get_label_for_prompt(prompt)
        
        # For BFS, we look for prompts with same label but no parameters
        df = self.history_manager.prompts_manager.df_prompts
        possible_prompts = df[(df['labels'] == label) & (df['params'].apply(lambda x: len(x) == 0))]['prompts'].tolist()
        
        probs = [self.history_manager.prompt_probabilities['no_params'][prompt] for prompt in possible_prompts]
        
        return self.sample_and_update(
            possible_prompts, 
            probs, 
            self.user_selection.numExploration,
            [None] * self.user_selection.numExploration
        )


# Usage
history_manager = HistoryLogger(prompts_manager=prompts_manager, org_id=ORG_ID, id=ID)
param_rec = ParamRecommendation(user_selection=user_selection_params, history_manager=history_manager)
print(user_selection_params.prompt)
print(param_rec.give_recommendation_dfs())
print(param_rec.give_recommendation_bfs())
