from pomegranate import *
from pomegranate.base import Node

# Ethnicity node has no parents
ethnicity = Node(DiscreteDistribution({
    "asian": 0.15,
    "black": 0.2,
    "hispanic": 0.3,
    "white": 0.35,
}), name="ethnicity")


#Gender node is conditional on ethnicity
gender = Node(ConditionalProbabilityTable([
    ["asian", "female", 0.55],
    ["black", "female", 0.6],
    ["hispanic", "female", 0.46],
    ["white", "female", 0.56],
    
    ["asian", "male", 0.45],
    ["black", "male", 0.40],
    ["hispanic", "male", 0.54],
    ["white", "male", 0.44],

], [ethnicity.distribution]), name="gender")



#Age node is conditional on ethnicity
age = Node(ConditionalProbabilityTable([
    ["asian", "child", 0.25],
    ["black", "child", 0.15],
    ["hispanic", "child", 0.30],
    ["white", "child", 0.23],
    
    ["asian", "adult", 0.75],
    ["black", "adult", 0.85],
    ["hispanic", "adult", 0.70],
    ["white", "adult", 0.77],

], [ethnicity.distribution]), name="age")


#Income node is conditional on ethnicity
income = Node(ConditionalProbabilityTable([
    ["asian", "low", 0.40],
    ["black", "low", 0.55],
    ["hispanic", "low", 0.30],
    ["white", "low", 0.35],
    
    ["asian", "high", 0.60],
    ["black", "high", 0.45],
    ["hispanic", "high", 0.70],
    ["white", "high", 0.65],

], [ethnicity.distribution]), name="income")



#Cough node is conditional on age,gender,income
cough = Node(ConditionalProbabilityTable([
    ["female", "child","low","cough", 0.35],
    ["female", "child","low","no cough", 0.65],
    
    ["female", "child","high","cough", 0.25],
    ["female", "child","high","no cough", 0.75],
    
    ["female", "adult","low","cough", 0.88],
    ["female", "adult","low","no cough", 0.12],
    
    ["female", "adult","high","cough", 0.05],
    ["female", "adult","high","no cough", 0.95],


    ["male", "child","low","cough", 0.15],
    ["male", "child","low","no cough", 0.85],
    
    ["male", "child","high","cough", 0.85],
    ["male", "child","high","no cough", 0.15],
    
    ["male", "adult","low","cough", 0.54],
    ["male", "adult","low","no cough", 0.46],
    
    ["male", "adult","high","cough", 0.64],
    ["male", "adult","high","no cough", 0.36],


], [gender.distribution, age.distribution, income.distribution]), name="cough")



#Fever node is conditional on age,gender,income
fever = Node(ConditionalProbabilityTable([
    ["female", "child","low","fever", 0.75],
    ["female", "child","low","no fever", 0.25],
    
    ["female", "child","high","fever", 0.40],
    ["female", "child","high","no fever", 0.60],
    
    ["female", "adult","low","fever", 0.44],
    ["female", "adult","low","no fever", 0.56],
    
    ["female", "adult","high","fever", 0.85],
    ["female", "adult","high","no fever", 0.15],


    ["male", "child","low","fever", 0.54],
    ["male", "child","low","no fever", 0.46],
    
    ["male", "child","high","fever", 0.64],
    ["male", "child","high","no fever", 0.36],
    
    ["male", "adult","low","fever", 0.27],
    ["male", "adult","low","no fever", 0.73],
    
    ["male", "adult","high","fever", 0.20],
    ["male", "adult","high","no fever", 0.80],

], [gender.distribution, age.distribution, income.distribution]), name="fever")


#Pneumonia node is conditional on cough and fever
pneumonia = Node(ConditionalProbabilityTable([
    ["cough", "fever","yes", 0.30],
    ["cough", "no fever","yes", 0.10],
    ["no cough", "fever","yes", 0.10],
    ["no cough", "no fever","yes", 0.001],

# we are just checking the chances of pneumonia taking place i.e yes

], [cough.distribution, fever.distribution]), name="pneumonia")


#Influenza node is conditional on cough and fever
influenza = Node(ConditionalProbabilityTable([
    ["cough", "fever","yes", 0.25],
    ["cough", "no fever","yes", 0.05],
    ["no cough", "fever","yes", 0.10],
    ["no cough", "no fever","yes", 0.00],
    
# we are just checking the chances of flu taking place i.e yes

], [cough.distribution, fever.distribution]), name="influenza")


# Create a Bayesian Network and add states FOR PNEUMONIA
model1 = BayesianNetwork()
model1.add_states(ethnicity,age,gender,income,cough,fever,pneumonia)

# Add edges connecting nodes

#ethnicity is connected to three demographics
model1.add_edge(ethnicity,gender)
model1.add_edge(ethnicity,age)
model1.add_edge(ethnicity,income)

# each demographic is connected to two symptoms
model1.add_edge(gender, cough)
model1.add_edge(gender, fever)

model1.add_edge(age, cough)
model1.add_edge(age, fever)

model1.add_edge(income, cough)
model1.add_edge(income, fever)

# Each symptom is connected to disease

model1.add_edge(cough, pneumonia)
model1.add_edge(fever, pneumonia)



# Create a Bayesian Network and add states FOR INFLUENZA
model2 = BayesianNetwork()
model2.add_states(ethnicity,age,gender,income,cough,fever,influenza)

# Add edges connecting nodes
#ethnicity is connected to three demographics
model1.add_edge(ethnicity,gender)
model1.add_edge(ethnicity,age)
model1.add_edge(ethnicity,income)

# each demographic is connected to two symptoms
model1.add_edge(gender, cough)
model1.add_edge(gender, fever)

model1.add_edge(age, cough)
model1.add_edge(age, fever)

model1.add_edge(income, cough)
model1.add_edge(income, fever)

# Each symptom is connected to 2 diseases
model2.add_edge(cough, influenza)
model2.add_edge(fever, influenza)

# Finalize model
model1.bake()
model2.bake()
