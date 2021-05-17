import offer
import claster
import algorithm
import scrapping

def main():
    offers = []
    texts = scrapping.download_and_get_text()
    # texts = scrapping.get_text()
    words_vector = scrapping.create_words_vector(texts)

    for i in range(50):
        new_offer = offer.Offer("imgs/" + str(i+1) + ".jpg", texts[i])
        new_offer.text_to_vector(words_vector)
        offers.append(new_offer)

    claster_array = []
    for e in offers:
        claster_array.append(claster.Claster([e]))
    
    x = algorithm.algorithm(claster_array)
    for a in x:
        print(a)

if __name__ == "__main__":
    main()