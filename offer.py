# import numpy as np
import cv2
import math


class Offer:
    def __init__(self, img_path, text):
        self.img_path = img_path
        self.text = text
        self.x = 0
        self.y = 0
        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        hist = cv2.calcHist([image], [0,1,2], None, [8,8,8], [0,256,0,256,0,256])
        self.hist = cv2.normalize(hist, hist).flatten()

    def compare_hist(self, other_hist):
        val = cv2.compareHist(self.hist, other_hist, cv2.HISTCMP_CORREL)
        return (1.0 - val) * 100.0

    def compare_vectors(self, other_vector):
        sum_of_products = 0
        for i in range(len(self.vector)):
            sum_of_products += self.vector[i] * other_vector[i]
        first_sqrt = 0
        second_sqrt = 0
        for i in range(len(self.vector)):
            first_sqrt += self.vector[i] ** 2
            second_sqrt += other_vector[i] ** 2
        first_sqrt = math.sqrt(first_sqrt)            
        second_sqrt = math.sqrt(second_sqrt)
        return 100.0 * (1.0 - (sum_of_products / (first_sqrt * second_sqrt)))

    def compare_offer(self, other_offer):
        x = self.compare_hist(other_offer.hist)
        y = self.compare_vectors(other_offer.vector)
        other_offer.x = x
        other_offer.y = y

    def text_to_vector(self, all_words):
        self.vector = []
        for _ in all_words:
            self.vector.append(0)
        split = self.text.split()
        for i in range(len(all_words)):
            for j in range(len(split)):
                if all_words[i] == split[j]:
                    self.vector[i] += 1
