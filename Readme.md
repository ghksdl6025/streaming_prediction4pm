# A framework for online business process outcome predictive monitoring

## General framework
<p align="center">
    <img src="./img/readme_img/general_framework_a.png">
    <br>
    <em>1.a)&nbsp Processing of an event without label</em>
    <img src="./img/readme_img/general_framework_b.png">
    <br>
    <em>1.b)&nbsp Processing of an event with label</em>
</p>

### In this figure, the processing of one event $e_{k,j}$ belonging to trace $\sigma_j$ is schematised.
---
First of all, the labels received are only used to train the models in the framework. The event <img src="https://render.githubusercontent.com/render/math?math=e_{k,j}">$e_{k,j}$ may either be the last of $\sigma_j$, i.e., length of $j$, in which case the label $y_j$ becomes known, or not. When an event is not the last one of its trace (see Fig. 1.a), it is used to generate a new prefix of $\sigma_j$ for prefix $k$. Then, a prediction $\hat{y}_{k,j}$ for the new prefix can be computed using the model for prefix $k$. Receiving the last event $e_{k,j}$, and its label (see Fig. 1.b) enables (i) to evaluate all the predictions $\hat{y}_j$ that have been generated for all prefixes $\sigma_j$ (evaluation before training), (ii) to update the models $pom_n$ owing to the availability of new labelled prefixes. Finally, it is possible (iii) to compute a new set of predicted labels $\hat{y}_{k,l}$, with $l\neq j$ and for all the prefixes for which a label has not been yet received (train and retest).  

## Sample scenario and performance indicator
<p align="center">
    <img src="./img/readme_img/Performance_indiciator_figure.png"><br>
    <br>
    <em>2)&nbsp Evaluation methods: supporting example</em>
</p>

### Fig. 2 exemplifies what stated above in the context of the proposed framework, considering 3 process cases and prefix length up to 3. 
---
Note that different versions of the same model pomk are generated along the considered timeline. In particular, a new version of $pom_k$ is generated when a new label $y_j$ for a case $\sigma_j$. For instance, in the example 3 different versions of $pom_1$ are generated. Second, new predictions for prefixes of length $k$ are generated each time a new version of $pom_k$ is available. In the example, receiving the label $y_{c1}$ of case c1 at t8 triggers (i) the creation
of a new version of $pom_1$ ($pom''_1$) and (ii) the generation of a new prediction $\hat{y}_{1,c3}$ for case c3, which is still running at t8. Finally, note that a prediction can only be evaluated when the corresponding label becomes available. In the example, the predictions generated for all the prefixes of case 3 cannot be evaluated because the label of case 3 has yet to be received at t8.


```
📦streaming_event_prediction4pm
 ┣ 📂data
 ┃ ┣ 📜bpic15.csv
 ┃ ┣ 📜bpic17.csv
 ┃ ┣ 📜iro5k.csv
 ┃ ┗ 📜road_traffic_fine_process.csv
 ┣ 📂img
 ┃ ┗ 📂readme_img
 ┃ ┃ ┣ 📜Performance_indiciator_figure.png
 ┃ ┃ ┣ 📜general_framework_a.png
 ┃ ┃ ┗ 📜general_framework_b.png
 ┣ 📂result
 ┃ ┣ 📂bpic15
 ┃ ┣ 📂bpic17
 ┃ ┣ 📂iro5k
 ┃ ┗ 📂road_traffic_fine_process
 ┣ 📜.gitignore
 ┣ 📜Readme.md
 ┣ 📜dataset_parameters.json
 ┣ 📜encoding.py
 ┣ 📜offline.ipynb
 ┣ 📜streaming_classification.ipynb
 ┗ 📜utils.py
 ```