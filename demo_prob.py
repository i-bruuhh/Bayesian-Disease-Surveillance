from demo_model import model1,model2

# Calculate probability for a pneumonia
probability_pneumonia = model1.probability([["hispanic", "adult", "female", "high", "no cough", "fever","yes"]])

# Calculate probability for flu 
probability_influenza = model2.probability([["hispanic", "adult", "female", "high", "no cough", "fever","yes"]])


print(probability_pneumonia)
print(probability_influenza)

