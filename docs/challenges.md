## Important NLP Challenges

What problems did I notice that NLP will need to handle?

- Job descriptions contain different types of information in the same text.
- Skills can have different names/abbreviations.
- Some information is structured in columns, while other information appears only inside job descriptions.
- Location names may have different spellings/names.
- The same skill can occur across multiple job roles.


## Experience Fields

There were 90 records where experience_min_yrs was greater
than experience_max_yrs.

The invalid records showed a strong systematic pattern,
particularly 77 records with values 13 and 8.

For the processed dataset, these values were swapped so that
the minimum experience is not greater than the maximum experience.

The original raw dataset was kept unchanged.


## final_match_score 
The problem is that our experience formula gives every 0-year job a perfect 1.0, even when the title says Lead, Manager, etc.

So the model is currently saying:

"Lead Data Scientist requiring 0 years = perfect experience match"

That's probably a dataset-quality issue + scoring limitation, not a problem with cosine similarity.

I think we should fix this before moving on.

We can add a small seniority compatibility rule:

intern / trainee / junior / associate → fresher-friendly
senior / lead / manager / principal / director → penalize for a fresher
normal data scientist / data analyst / ML engineer → neutral

This will make recommendations much more realistic without making the project unnecessarily complicated.


## at the time of deployment

"I converted the high-dimensional job-skill matrix to a sparse representation because most skill features were zero, significantly reducing memory and storage requirements."