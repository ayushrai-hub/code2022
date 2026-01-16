# -----------------------------  common imports  -----------------------------
from typing import List, Dict, Any, Sequence, Optional
import numpy as np
from pydantic import BaseModel


# ----------------------------------------------------------------------------
#  BASE RECOMMENDER – all shared logic lives here
# ----------------------------------------------------------------------------
class MainRecommender(BaseModel):
    user_selection: "UserSelection"
    history_manager: "HistoryLogger"

    # ------------------------------------------------------------------------
    #  Public API kept identical to your original code
    # ------------------------------------------------------------------------
    def give_recommendation_dfs(self) -> List[str]:
        """
        Depth‑first style recommendation (a.k.a. ‘deep dive’).
        Implemented in subclasses by specifying:
        * _candidate_prompts_dfs()
        * _probability_for_prompt(prompt)
        """
        return self._recommend(
            candidate_prompts=self._candidate_prompts_dfs(),
            sample_size=self.user_selection.numDeepDive,
        )

    def give_recommendation_bfs(self) -> List[str]:
        """
        Breadth‑first style recommendation (a.k.a. ‘exploration’).
        Implemented in subclasses by specifying:
        * _candidate_prompts_bfs()
        * _probability_for_prompt(prompt)
        """
        return self._recommend(
            candidate_prompts=self._candidate_prompts_bfs(),
            sample_size=self.user_selection.numExploration,
        )

    # ------------------------------------------------------------------------
    #  Methods subclasses MUST implement
    # ------------------------------------------------------------------------
    def _candidate_prompts_dfs(self) -> List[str]:
        raise NotImplementedError

    def _candidate_prompts_bfs(self) -> List[str]:
        raise NotImplementedError

    def _probability_for_prompt(self, prompt: str) -> float:
        """Return an un‑normalised probability for *prompt*."""
        raise NotImplementedError

    def _params_for_history_update(self, prompt: str) -> Optional[Dict[str, Any]]:
        """
        What parameter dict should be written to history for this prompt?
        (None if no parameters).  Default is None.
        """
        return None

    # ------------------------------------------------------------------------
    #  Helpers that are the SAME for every recommender
    # ------------------------------------------------------------------------
    def _standardise_probabilities(self, probs: Sequence[float]) -> List[float]:
        total = sum(probs)
        if total == 0:
            # fall back to a uniform distribution
            return [1 / len(probs)] * len(probs)
        return [p / total for p in probs]

    def _update_history(self, prompts: List[str]) -> None:
        params = [self._params_for_history_update(p) for p in prompts]
        self.history_manager.update_prompt_probabilities(
            prompts, params=params, mode="recommendations"
        )

    def _recommend(self, candidate_prompts: List[str], sample_size: int) -> List[str]:
        if not candidate_prompts:
            return []

        probs = [self._probability_for_prompt(p) for p in candidate_prompts]
        probs = self._standardise_probabilities(probs)

        chosen = np.random.choice(
            candidate_prompts, size=sample_size, replace=False, p=probs
        ).tolist()

        self._update_history(chosen)
        return chosen


# ----------------------------------------------------------------------------
#  NO‑PARAMS RECOMMENDER
# ----------------------------------------------------------------------------
class NoParamsRecommendation(MainRecommender):
    # -- internal helpers -----------------------------------------------------
    @property
    def _df(self):
        return self.history_manager.prompts_manager.df_prompts

    # -- probability comes from 'no_params' bucket ----------------------------
    def _probability_for_prompt(self, prompt: str) -> float:
        return self.history_manager.prompt_probabilities["no_params"][prompt]

    # -- candidate sets -------------------------------------------------------
    def _candidate_prompts_dfs(self) -> List[str]:
        """Same label, same (empty) params."""
        label = self._df.loc[self._df.prompts == self.user_selection.prompt, "labels"].iat[0]
        mask = (self._df.labels == label) & (self._df.params.apply(len) == 0)
        return self._df.loc[mask, "prompts"].tolist()

    def _candidate_prompts_bfs(self) -> List[str]:
        """
        Closest neighbouring cluster that also has no parameters.
        We reuse your distance dict logic.
        """
        df = self._df
        label = df.loc[df.prompts == self.user_selection.prompt, "labels"].iat[0]

        # find the closest cluster to *label*
        distances = {
            other: dist
            for (l1, l2), dist in self.history_manager.prompts_manager.cluster_distances.items()
            if label in (l1, l2) and other := (l2 if l1 == label else l1)
        }
        if not distances:
            return []  # no neighbour – return empty list

        closest_label = min(distances, key=distances.get)
        mask = (df.labels == closest_label) & (df.params.apply(len) == 0)
        return df.loc[mask, "prompts"].tolist()


# ----------------------------------------------------------------------------
#  PARAM‑BASED RECOMMENDER
# ----------------------------------------------------------------------------
class ParamRecommendation(MainRecommender):
    # -- cached references ----------------------------------------------------
    @property
    def _df(self):
        return self.history_manager.prompts_manager.df_prompts

    # -- probability lookup ---------------------------------------------------
    def _probability_for_prompt(self, prompt: str) -> float:
        key_param = self._key_param_name(prompt)
        key_value = self.user_selection.parameters[key_param]

        # lazily create probability entry if missing
        prob_dict = self.history_manager.prompt_probabilities["params"][prompt][key_param]
        prob_dict.setdefault(key_value, 1)
        return prob_dict[key_value]

    # -- params written to history -------------------------------------------
    def _params_for_history_update(self, prompt: str):
        key_param = self._key_param_name(prompt)
        return {key_param: self.user_selection.parameters[key_param]}

    # -- candidate prompts ----------------------------------------------------
    def _key_param_name(self, prompt: str) -> str:
        """Assumes exactly one parameter in df for this prompt."""
        return self._df.loc[self._df.prompts == prompt, "params"].iat[0][0]

    def _candidate_prompts_dfs(self) -> List[str]:
        prompt = self.user_selection.prompt
        key_param = self._key_param_name(prompt)
        df = self._df
        mask = df.params.apply(lambda lst: lst == [key_param])
        return df.loc[mask, "prompts"].tolist()

    def _candidate_prompts_bfs(self) -> List[str]:
        """
        When exploring, re‑use the logic of NoParamsRecommendation:
        find prompts in the same cluster *without* parameters.
        """
        df = self._df
        label = df.loc[df.prompts == self.user_selection.prompt, "labels"].iat[0]
        mask = (df.labels == label) & (df.params.apply(len) == 0)
        return df.loc[mask, "prompts"].tolist()


# ----------------------------------------------------------------------------
#  USAGE EXAMPLE (unchanged)
# ----------------------------------------------------------------------------
history_manager = HistoryLogger(
    prompts_manager=prompts_manager, org_id=ORG_ID, id=ID
)

param_rec = ParamRecommendation(
    user_selection=user_selection_params, history_manager=history_manager
)

print(user_selection_params.prompt)
print(param_rec.give_recommendation_dfs())
print(param_rec.give_recommendation_bfs())
