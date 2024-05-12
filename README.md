Approached used in this project is
Modular Approach with Notebooks

Implementing Modular Approach with Notebooks
In the modular approach using notebooks, each major task or component of your data processing pipeline is encapsulated in its own notebook. This setup allows you to maintain a clear separation of concerns while taking advantage of the interactive and visual capabilities of notebooks.

How to Set Up Modular Notebooks
Organize Notebooks by Task: Similar to how you would organize scripts, create individual notebooks for each major task, such as:

Text_Cleaning.ipynb
Tokenization.ipynb
Noun_Extraction.ipynb
Word_Embedding.ipynb
Create a Master Notebook: Have a master notebook that summarizes or orchestrates the workflow, potentially running other notebooks in sequence or linking to them for detailed steps.

Running Notebooks Sequentially
To automate the running of one notebook from another, you can use the nbconvert and ExecutePreprocessor from Jupyter:

Advantages of Using Notebooks
Interactivity: Notebooks are highly interactive, allowing you to run code blocks independently and see results immediately.
Visualization: Direct support for visualizations makes notebooks ideal for exploratory data analysis.
Documentation: The ability to combine code, outputs, and narrative text makes notebooks an excellent tool for documenting the data analysis process.
Differences Between Notebooks and Scripts
Reproducibility: Scripts are generally more reproducible across different environments because they are less dependent on the interactive state of the environment, unlike notebooks which can be run out of order or contain hidden state.

Version Control: Notebooks can be more challenging to version control due to their mix of code, output, and binary data. Git diffs of notebook files can be cluttered with changes in the output cells.

Execution: Scripts can be more easily automated and integrated into larger software systems or data pipelines. They are straightforward to run from the command line or within other scripts.

Modularity: While both approaches support modularity, scripts are typically easier to reuse as modules in other scripts or applications due to their straightforward import mechanism.

Conclusion
Choosing between notebooks and scripts often comes down to the specific needs of your project and your workflow preferences. If your work heavily involves data exploration, visualization, and requires presenting findings interactively, notebooks could be the better choice. For projects that require high levels of automation, reproducibility, and integration into production environments, scripts might be more advantageous.

For a research-oriented project like yours where documentation and step-by-step analysis are critical, using notebooks for each phase of the process could provide a beneficial balance of modularity, documentation, and interactivity.
