from GraphEmbedding import GraphEmbedding


def runTest():
    print("Initializing (it can take long) ...", end="")

    graphEmbed = GraphEmbedding()

    print("done")

    while True:
        print("Enter a number (-1 to exit): ")
        input1 = int(input())
        if input1 == -1:
            break
        graphEmbed.getNearest(input1)

    print("Goodbye!")


if __name__ == "__main__":
    runTest()