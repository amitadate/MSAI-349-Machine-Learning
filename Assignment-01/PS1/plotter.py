import node
import parse
import ID3
import random
import math
import matplotlib.pyplot as plt


def getAverages(inFile):
  withP = []
  withoutP = []
  TrainingLength = []

  data = parse.parse(inFile)

  for a in range(10, 300 ):
    TrainingLength.append(a)
    withPruning = []
    withoutPruning = []
    x = int(0.7 * a)

    for i in range(100):

      random.shuffle(data)

      group = data[:a]  # taking a number of examples in training + validation set
      train = group[:x]  # splitting 70 30
      valid = group[x:]  # rest
      test = data[a:]   

      treeNP = ID3.ID3(group, 'democrat')
      accNP = ID3.test(treeNP, test)

      withoutPruning.append(accNP)

      treeWP = ID3.ID3(train, 'democrat')
      ID3.prune(treeWP, valid)
      accWP = ID3.test(treeWP, test)

      withPruning.append(accWP)

    averagewith = sum(withPruning) / len(withPruning)

    withP.append(averagewith)
    averageWO = sum(withoutPruning) / len(withoutPruning)

    withoutP.append(averageWO)

  return withP, withoutP, TrainingLength


y1, y2, x = getAverages('house_votes_84.data')

plt.plot(x, y1, color='skyblue', label ='With Prune')
plt.plot(x, y2, color='magenta', label ='Without Prune')
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),  shadow=True, ncol=2)

plt.xlabel('Number of training examples')
plt.ylabel('Accuracy on test data')
plt.show()
