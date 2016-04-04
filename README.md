Average Degree of Twitter Hashtag Graph -- Implemented by Yanhuan Li
===========================================================

# Table of Contents
1. [Implementation Summary](README.md#implement-summary)
2. [Details of Implementation](README.md#details-of-implementation)
   1. [Representing Hashtag Graph with Adjacency Dictionary(AD)](README.md#Representing Hashtag Graph with Adjacency Dictionary(AD))
        1. [Detailed data structure in Adjacency Dictionary](README.md#Detailed data structure in Adjacency Dictionary)
        2. [Insert and Delete Edges in Hashtag Graph](README.md#Insert and Delete Edges in Hashtag Graph)
   2. [Maintaining Data within the 60 Second Window by Time Pointer](README.md#Maintaining Data within the 60 Second Window by Time Pointer)
3. [Directory Structure](README.md#Directory Structure)
4. [How to Test and Run the Code](README.md#How to Test and Run the Code)



## Implementation Summary
[Back to Table of Contents](README.md#table-of-contents)

This challenge requires:

Develop a tool that analyze the community of Twitter users. Specifically:
  1. Calculate the average degree of a vertex in a Twitter hashtag graph for the last 60 seconds
  2. Update this each time a new tweet appears.  Consequently I will thus be calculating the average degree over a 60-second sliding window.


## Details of Implementation
[Back to Table of Contents](README.md#table-of-contents)

Before constructing the Twitter hashtag graph, I need clean and extract the useful tweets from raw JSON tweets who satisfied:
1. At lease one hashtag exists in the tweet, that means remove tweets with empty hashtag texts.
2. Remove rate limit messages from the input `tweets.txt`.

Once I got all useful tweets from raw JSON input, I extrated `'created_at'` and `'entities'` as my timestamps and hashtags information, respectively.

### Representing Hashtag Graph with Adjacency Dictionary(AD)
[Back to Table of Contents](README.md#table-of-contents)

By using AD, two main problems can be avoided:
* Repeated edge arriving afterwards will evict the old same edge, which by other methods may cause this entire edge be removed improperly.
* Each edge in the graph can be easily visited by using keywords `word_i` and `word_j` in the dictionary `hs_graph`.

#### Detailed data structure in Adjacency Dictionary

AD is a modified representation of Adjacency Matrix data structure, which is constructed from edges.
Since each row or column denotes distinct hashtag, it will thus always be a symmetric matrix. For example at the beginning, connections exist like:

    Spark <-> Apache
    Apache <-> Hadoop

Each connection will be denoted as an edge in the graph, `edge1 = (Spark, Apache)` and `edge2 = (Apahe, Hadoop)`. In the matrix, it will be:

            Spark   Apache   Hadoop
    Spark     0       1        0
    Apache    1       0        1
    Hadoop    0       1        0
Each distinct hashtag coming in will be denoted as a new entry named by the hasgtag text in this matrix. Wherever a connection (`text1`, `text2`) exists, i.e.: `text1` and `text2` appeared in one tweet, the element increased by 1 correspondingly in the matrix. Therefore, if the matrix is like:

            Spark   Apache   Hadoop
    Spark     0       2        0
    Apache    2       0        1
    Hadoop    0       1        0
By using AD method, the graph structure should be like:

    {
     "Spark" : { "Apache": 2}
     "Apache": { "Spark": 2, "Hadoop": 1}
     "Hadoop": { "Apache": 1}
     }
As we can see in the structure, this data is implemented by a dictionary( `hs_graph` in my codes), which saved a lot of space since we only stored edges with non-zero values.

#### Insert and Delete Edges in Hashtag Graph
Another key module implemented in my tool is to insert and delete edges in te graph, once we constructed a twitter graph for the last 60 seconds, every time a new tweet coming in (as long as it's in 60s window), new vertices and edges need to be inserted and earliest vertices and edges that are out of 60s window need to be removed.

* Insert edges in Hashtag Garph is implemented by `insert_in_graph`. Cases that needs to insert new edges are:

    1. Constructing the hashtag graph for the last 60s
    2. Updating the graph whenever a valid new tweet arrives either by the right time order or out of order yet within the 60s window.

* Examine the deleted old edges from Hashtag Grpah is implemented by `delete_and_update_degree`. In the second case above, whenever a new tweet coming in with the right time order, the earliest tweets need to be examined and deleted to maintain the 60s window.


### Maintaining Data within the 60 Second Window by Time Pointer
[Back to Table of Contents](README.md#table-of-contents)

In my tool, I used the latest timestamp (`ts_ending`) as my time pointer. Every time a new tweet with a new timestamp (`ts_new`) arrives in, there will be always three cases:
1. ts_new > ts_ending, then new time pointer should be assigned by ts_new.
2. ts_new < ts_ending and ts_new is in 60s window, then `ts_ending` remains the same, yet the only change maybe determined by delete old tweets or not.
3. ts_new < ts_enidng and ts_new is out of 60s window, pass.


## Directory Structure
[Back to Table of Contents](README.md#table-of-contents)

	├── README.md 
	├── run.sh
	├── src
	│   ├── average_degree.java
	|   └── tweet_processor.py
	├── tweet_input
	│   └── tweets.txt
	├── tweet_output
	│   └── output.txt
	└── insight_testsuite
	    ├── run_tests.sh
	    ├── results.txt
	    ├── tests
	    │   ├── test-2-tweets-all-distinct
	    │   │   ├── tweet_input
	    │   │   │   └── tweets.txt
	    │   │   └── tweet_output
	    │   │       └── output.txt
	    │   └── your-own-test
	    │       ├── tweet_input
	    │       │   └── tweets.txt
	    │       └── tweet_output
	    │           └── output.txt
	    └── temp
	        ├──src
	        ├──tweet_input
	        └──tweet_output

## How to Test and Run the Code
[Back to Table of Contents](README.md#table-of-contents)

* bash run_tests.sh under insight_testsuite
* bash run.sh under root directory
* In order to run my code, you need to to run any program, you need some general python libraries, like json, os, sys, datetime.



