from GraphEmbedding import GraphEmbedding


def runTest():
    print("Initializing (it can take long) ...", end="")

    graphEmbed = GraphEmbedding()

    print("done")

    while True:
        print("Enter a name of a Facebook page (enter the letter 'q' to quit): ")
        input1 = str(input())
        if input1 == "Q" or input1 == "q":
            break
        index = graphEmbed.doWeHaveIt(input1)
        if index != -1:
            graphEmbed.getNearest(index)

    print("Goodbye!")


if __name__ == "__main__":
    runTest()
