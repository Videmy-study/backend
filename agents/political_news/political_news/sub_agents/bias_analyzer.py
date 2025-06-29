# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Bias Analyzer Sub-Agent: Analyzes news articles for bias and credibility."""

import logging
import re
from typing import List, Dict, Any, Optional

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import bias_analyzer_prompt

MODEL = "gemini-2.5-pro"

logger = logging.getLogger(__name__)

class BiasAnalyzer:
    """Analyzes news articles for bias and credibility."""
    
    # Known biased terms and phrases
    BIASED_TERMS = {
        "left_wing": [
            "progressive", "liberal agenda", "socialist", "radical left",
            "woke", "cancel culture", "defund the police", "open borders"
        ],
        "right_wing": [
            "conservative agenda", "far-right", "alt-right", "MAGA",
            "America first", "traditional values", "pro-life", "gun rights"
        ],
        "emotional": [
            "outrageous", "shocking", "devastating", "amazing", "incredible",
            "terrible", "wonderful", "horrible", "fantastic", "disgusting"
        ],
        "partisan": [
            "democrats say", "republicans claim", "liberals argue", "conservatives believe",
            "the left", "the right", "blue state", "red state"
        ]
    }
    
    # Known credible sources
    CREDIBLE_SOURCES = {
        "high": [
            "reuters", "associated press", "ap", "bbc news", "npr", "pbs",
            "c-span", "wall street journal", "new york times", "washington post",
            "usa today", "cnn", "fox news", "msnbc", "abc news", "cbs news",
            "nbc news", "politico", "roll call", "the hill"
        ],
        "medium": [
            "bloomberg", "forbes", "time", "newsweek", "the atlantic",
            "the new yorker", "national review", "the nation", "mother jones"
        ],
        "low": [
            "breitbart", "daily caller", "daily beast", "huffpost", "vox",
            "buzzfeed news", "vice news", "salon", "alternet"
        ]
    }
    
    def analyze_article_bias(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a single article for bias and credibility."""
        title = article.get("title", "").lower()
        description = article.get("description", "").lower()
        content = article.get("content", "").lower()
        source = article.get("source", "").lower()
        
        # Combine all text for analysis
        full_text = f"{title} {description} {content}"
        
        # Analyze for biased language
        bias_indicators = self._detect_bias_indicators(full_text)
        
        # Analyze source credibility
        credibility_score = self._assess_source_credibility(source)
        
        # Analyze emotional language
        emotional_score = self._detect_emotional_language(full_text)
        
        # Analyze partisan language
        partisan_score = self._detect_partisan_language(full_text)
        
        # Calculate overall bias score
        overall_bias_score = self._calculate_bias_score(
            bias_indicators, credibility_score, emotional_score, partisan_score
        )
        
        return {
            "article_title": article.get("title", ""),
            "source": article.get("source", ""),
            "bias_indicators": bias_indicators,
            "credibility_score": credibility_score,
            "emotional_score": emotional_score,
            "partisan_score": partisan_score,
            "overall_bias_score": overall_bias_score,
            "bias_category": self._categorize_bias(overall_bias_score),
            "recommendations": self._generate_recommendations(
                bias_indicators, credibility_score, overall_bias_score
            )
        }
    
    def _detect_bias_indicators(self, text: str) -> Dict[str, Any]:
        """Detect various types of bias in the text."""
        indicators = {
            "left_wing_terms": [],
            "right_wing_terms": [],
            "emotional_terms": [],
            "partisan_terms": [],
            "loaded_language": [],
            "factual_claims": [],
            "opinion_indicators": []
        }
        
        # Check for biased terms
        for bias_type, terms in self.BIASED_TERMS.items():
            for term in terms:
                if term in text:
                    if bias_type == "left_wing":
                        indicators["left_wing_terms"].append(term)
                    elif bias_type == "right_wing":
                        indicators["right_wing_terms"].append(term)
                    elif bias_type == "emotional":
                        indicators["emotional_terms"].append(term)
                    elif bias_type == "partisan":
                        indicators["partisan_terms"].append(term)
        
        # Detect loaded language (strong emotional words)
        loaded_patterns = [
            r'\b(clearly|obviously|undoubtedly|certainly|definitely)\b',
            r'\b(always|never|everyone|nobody|all|none)\b',
            r'\b(disaster|catastrophe|miracle|revolutionary|groundbreaking)\b'
        ]
        
        for pattern in loaded_patterns:
            matches = re.findall(pattern, text)
            indicators["loaded_language"].extend(matches)
        
        # Detect factual claims vs opinions
        factual_patterns = [
            r'\b(according to|data shows|study finds|research indicates)\b',
            r'\b(statistics|figures|numbers|percent|percentage)\b',
            r'\b(official|confirmed|verified|documented)\b'
        ]
        
        opinion_patterns = [
            r'\b(i think|i believe|in my opinion|it seems|appears)\b',
            r'\b(many say|some argue|critics claim|supporters believe)\b',
            r'\b(should|could|would|might|may)\b'
        ]
        
        for pattern in factual_patterns:
            matches = re.findall(pattern, text)
            indicators["factual_claims"].extend(matches)
        
        for pattern in opinion_patterns:
            matches = re.findall(pattern, text)
            indicators["opinion_indicators"].extend(matches)
        
        return indicators
    
    def _assess_source_credibility(self, source: str) -> Dict[str, Any]:
        """Assess the credibility of the news source."""
        source_lower = source.lower()
        
        # Check against known credible sources
        for credibility_level, sources in self.CREDIBLE_SOURCES.items():
            for known_source in sources:
                if known_source in source_lower:
                    return {
                        "level": credibility_level,
                        "score": {"high": 0.9, "medium": 0.6, "low": 0.3}[credibility_level],
                        "reason": f"Known {credibility_level} credibility source"
                    }
        
        # Default assessment for unknown sources
        return {
            "level": "unknown",
            "score": 0.5,
            "reason": "Unknown source - requires additional verification"
        }
    
    def _detect_emotional_language(self, text: str) -> float:
        """Detect the level of emotional language in the text."""
        emotional_terms = self.BIASED_TERMS["emotional"]
        emotional_count = sum(1 for term in emotional_terms if term in text)
        
        # Normalize by text length
        word_count = len(text.split())
        if word_count == 0:
            return 0.0
        
        emotional_ratio = emotional_count / word_count
        return min(emotional_ratio * 100, 1.0)  # Cap at 1.0
    
    def _detect_partisan_language(self, text: str) -> float:
        """Detect the level of partisan language in the text."""
        partisan_terms = self.BIASED_TERMS["partisan"]
        partisan_count = sum(1 for term in partisan_terms if term in text)
        
        # Normalize by text length
        word_count = len(text.split())
        if word_count == 0:
            return 0.0
        
        partisan_ratio = partisan_count / word_count
        return min(partisan_ratio * 50, 1.0)  # Cap at 1.0
    
    def _calculate_bias_score(self, bias_indicators: Dict, credibility_score: Dict, 
                            emotional_score: float, partisan_score: float) -> float:
        """Calculate an overall bias score for the article."""
        # Base score starts with credibility
        base_score = credibility_score["score"]
        
        # Adjust for bias indicators
        bias_penalty = 0.0
        
        # Penalize for emotional language
        bias_penalty += emotional_score * 0.3
        
        # Penalize for partisan language
        bias_penalty += partisan_score * 0.4
        
        # Penalize for loaded language
        loaded_penalty = len(bias_indicators["loaded_language"]) * 0.05
        bias_penalty += min(loaded_penalty, 0.2)
        
        # Penalize for opinion indicators vs factual claims
        opinion_ratio = len(bias_indicators["opinion_indicators"]) / max(len(bias_indicators["factual_claims"]), 1)
        bias_penalty += min(opinion_ratio * 0.2, 0.3)
        
        # Calculate final score (0 = highly biased, 1 = unbiased)
        final_score = max(0.0, base_score - bias_penalty)
        return round(final_score, 2)
    
    def _categorize_bias(self, bias_score: float) -> str:
        """Categorize the article based on bias score."""
        if bias_score >= 0.8:
            return "Low Bias - Highly Credible"
        elif bias_score >= 0.6:
            return "Moderate Bias - Generally Reliable"
        elif bias_score >= 0.4:
            return "High Bias - Exercise Caution"
        else:
            return "Very High Bias - Questionable Reliability"
    
    def _generate_recommendations(self, bias_indicators: Dict, credibility_score: Dict, 
                                overall_bias_score: float) -> List[str]:
        """Generate recommendations for using the article."""
        recommendations = []
        
        if overall_bias_score < 0.4:
            recommendations.append("Cross-reference with multiple sources")
            recommendations.append("Verify factual claims independently")
            recommendations.append("Consider alternative viewpoints")
        
        if len(bias_indicators["emotional_terms"]) > 3:
            recommendations.append("Article contains emotional language - focus on facts")
        
        if len(bias_indicators["partisan_terms"]) > 2:
            recommendations.append("Article shows partisan bias - seek balanced coverage")
        
        if credibility_score["level"] == "unknown":
            recommendations.append("Source credibility unknown - verify independently")
        
        if len(bias_indicators["opinion_indicators"]) > len(bias_indicators["factual_claims"]):
            recommendations.append("Article contains more opinion than fact")
        
        if not recommendations:
            recommendations.append("Article appears balanced and credible")
        
        return recommendations

def analyze_news_bias(articles: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze a list of news articles for bias and credibility."""
    analyzer = BiasAnalyzer()
    
    analyzed_articles = []
    total_bias_score = 0.0
    bias_distribution = {
        "Low Bias": 0,
        "Moderate Bias": 0,
        "High Bias": 0,
        "Very High Bias": 0
    }
    
    for article in articles:
        analysis = analyzer.analyze_article_bias(article)
        analyzed_articles.append(analysis)
        total_bias_score += analysis["overall_bias_score"]
        
        # Count bias categories
        category = analysis["bias_category"]
        if "Low Bias" in category:
            bias_distribution["Low Bias"] += 1
        elif "Moderate Bias" in category:
            bias_distribution["Moderate Bias"] += 1
        elif "High Bias" in category:
            bias_distribution["High Bias"] += 1
        else:
            bias_distribution["Very High Bias"] += 1
    
    # Calculate average bias score
    avg_bias_score = total_bias_score / len(articles) if articles else 0.0
    
    # Generate overall recommendations
    overall_recommendations = []
    if avg_bias_score < 0.6:
        overall_recommendations.append("Overall coverage shows bias - seek diverse sources")
    if bias_distribution["High Bias"] + bias_distribution["Very High Bias"] > len(articles) * 0.5:
        overall_recommendations.append("Majority of articles show bias - verify information")
    if bias_distribution["Low Bias"] > len(articles) * 0.7:
        overall_recommendations.append("Most articles appear credible and balanced")
    
    return {
        "total_articles_analyzed": len(articles),
        "average_bias_score": round(avg_bias_score, 2),
        "bias_distribution": bias_distribution,
        "overall_recommendations": overall_recommendations,
        "individual_analyses": analyzed_articles,
        "analysis_summary": {
            "most_credible_sources": [a["source"] for a in analyzed_articles if a["overall_bias_score"] >= 0.8],
            "least_credible_sources": [a["source"] for a in analyzed_articles if a["overall_bias_score"] < 0.4],
            "common_bias_indicators": _get_common_bias_indicators(analyzed_articles)
        }
    }

def _get_common_bias_indicators(analyzed_articles: List[Dict[str, Any]]) -> Dict[str, int]:
    """Get the most common bias indicators across all articles."""
    indicator_counts = {}
    
    for analysis in analyzed_articles:
        for indicator_type, indicators in analysis["bias_indicators"].items():
            for indicator in indicators:
                key = f"{indicator_type}: {indicator}"
                indicator_counts[key] = indicator_counts.get(key, 0) + 1
    
    # Return top 10 most common indicators
    sorted_indicators = sorted(indicator_counts.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_indicators[:10])

bias_analyzer_agent = LlmAgent(
    name="bias_analyzer_agent",
    model=MODEL,
    description=(
        "Analyzes news articles for bias, credibility, and reliability. "
        "Provides detailed assessments of source credibility, emotional language, "
        "partisan bias, and overall reliability scores."
    ),
    instruction=bias_analyzer_prompt.BIAS_ANALYZER_PROMPT,
    output_key="bias_analysis",
    tools=[analyze_news_bias],
) 