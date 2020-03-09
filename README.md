# Simple_Chinese_metaphor_identification_by_tongyicilin

 a simple chinese metaphor identification with abstractness of Tongyicilin

 Classifying the metaphority of verb by three steps:

 1) extract the subject and object of verbs (if exist)

 2) obtain the semantic codes of them from Tongyicilin. Use the code of similar word for nonexistent words in Tongyicilin. The cosine similarity between words calculated with word2vec.

 3) the abstractness/concreteness of codes are tagged manually. The abstract of subject/object can be obtained via codes. The verb is labeled as metaphor when its subject/object is abstract.
