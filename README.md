<p align="center">
  <img src="pic.jpg" width="1000">
  <br />
  <br />
</p> 

# ASGN

The official implementation of the ASGN model.
Orginal paper: ASGN: An Active Semi-supervised Graph Neural Network for Molecular Property Prediction. KDD'2020 Accepted. 

# Project Structure
+ `base_model`: Containing SchNet and training code for QM9 and OPV datasets. 

+ `rd_learn`: A baseline using random data selection.

+ `geo_learn`: Geometric method of active learning like k_center.

+ `qbc_learn`: Active learning by using query by committee.

+ `utils`: Dataset preparation and utils functions.
+ `baselines`: Active learning baselines from [google's implementation](https://github.com/google/active-learning).

+ `single_model_al`: contains several baseline models and our method ASGN (in file wsl_al.py)

+ `exp`: Experiments loggings.


# How to learn
- You need to modify self.PATH in config.py depending on your environment.
```
1. qm9 download (below link)
https://figshare.com/articles/dataset/Data_for_6095_constitutional_isomers_of_C7H10O2/1057646?backTo=/collections/Quantum_chemistry_structures_and_properties_of_134_kilo_molecules/978904
2. PYTHONPATH=. python utils/pre/qm9_predata.py
3. PYTHONPATH=. python utils/pre/pre_qm.py
4. PYTHONPATH=. python single_model_al/wsl_al.py 
```



# Citing ASGN
If you use ASGN in your research, please use the following BibTex.
```
@inproceedings{hao2020asgn,
  title={ASGN: An Active Semi-supervised Graph Neural Network for Molecular Property Prediction},
  author={Hao, Zhongkai and Lu, Chengqiang and Huang, Zhenya and Wang, Hao and Hu, Zheyuan and Liu, Qi and Chen, Enhong and Lee, Cheekong},
  booktitle={Proceedings of the 26th ACM SIGKDD International Conference on Knowledge Discovery \& Data Mining},
  pages={731--752},
  year={2020}
}
```


# IDEAS
- Swav
    - Sinkhorn problem end2end 로 바꾸기.
- Multiple clustering 
    - 다양한 기준으로 클러스터링한다?
- Signal from pseudo label
    - student 성능 기반으로 signal 얻기