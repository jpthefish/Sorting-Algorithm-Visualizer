from tkinter import *
import random
import time

#Array variables
MAX_ARRAY_SIZE = 200
arrayValues = [0 for i in range(MAX_ARRAY_SIZE)]
barWidth = 1.0
playbackSpeed = 9.0

#Colors
BLUE = '#4B8BC0'
DARKBLUE = '#4682B4'
DARKESTBLUE = '#355C96'
RED = '#E2635B'
GRAY = '#DDDDDD'

def main():
    #UI
    root = Tk()
    root.title("Sorting Algorithm Visualizer")
    root.geometry("900x575")

    #Initialize and set array values on canvas
    arrayCanvas = Canvas(root, width=750, height=500)
    arrayCanvas.pack(side=BOTTOM)
    arrayValuesAsLines = [arrayCanvas.create_line(i, 500, i, 500 - arrayValues[i], fill=BLUE) for i in range(MAX_ARRAY_SIZE)]

    def initializeArray(arraySize='150'):
        i = 0
        global barWidth
        global arrayValues
        arrayValues = [random.randint(20, 500) for i in range(int(arraySize))]
        barWidth = 675/float(arraySize)
        arrayCanvas.delete('all')

        for i in range(int(arraySize)):
            arrayValuesAsLines[i] = arrayCanvas.create_line(barWidth * (i + 1) + 1, 500, barWidth * (i + 1), 500 - arrayValues[i], fill=BLUE, width=barWidth)
        
    def dynamicDraw(arrayFillColor):
        i = 0
        global barWidth
        global arrayValues
        barWidth = 675/float(len(arrayValues))
        arrayCanvas.delete('all')

        for i in range(len(arrayValues)):
            arrayValuesAsLines[i] = arrayCanvas.create_line(barWidth * (i + 1) + 1, 500, barWidth * (i + 1), 500 - arrayValues[i], fill=arrayFillColor[i], width=barWidth)

        arrayCanvas.update()

    #Handover to algorithms
    def startSorting():
        selectedSortingMethod = textInOptionMenu.get()
        if selectedSortingMethod == 'Bubble Sort':
            bubbleSort()
        elif selectedSortingMethod == 'Merge Sort':
            mergeSort(0, len(arrayValues) - 1)
        elif selectedSortingMethod == 'Quick Sort':
            quickSort(0, len(arrayValues) - 1)
        else:
            heapSort()

    #Initialize navigation elements
    navigationFrame = Frame(root)
    generateArrayButton = Button(navigationFrame, text='Generate New Array', command=initializeArray)
    sortSelectionText = Label(navigationFrame, text='Sorting Algorithm:')
    textInOptionMenu = StringVar(root)
    textInOptionMenu.set("Heap Sort")
    sortSelectionOptionMenu = OptionMenu(navigationFrame, textInOptionMenu, "Heap Sort", "Merge Sort", "Quick Sort", "Bubble Sort")
    arraySizeText = Label(navigationFrame, text='Array Size:')
    arraySizeScale = Scale(navigationFrame,  from_=15, to=MAX_ARRAY_SIZE, orient=HORIZONTAL, sliderlength=15, command=initializeArray)
    arraySizeScale.set(100)
    sortButton = Button(navigationFrame, text='Sort This Array', highlightbackground=GRAY, command=startSorting)

    navigationFrame.pack()
    generateArrayButton.pack(side=LEFT, padx=5)
    sortSelectionText.pack(side=LEFT, padx=5)
    sortSelectionOptionMenu.pack(side=LEFT, padx=5)
    arraySizeText.pack(side=LEFT, padx=5)
    arraySizeScale.pack(side=LEFT, padx=5)
    sortButton.pack(side=LEFT, padx=5)

    #ALGORITHMS

    #Heap sort
    def heapify(n, i):
        largest = i
        left = 2*i+1
        right = 2*i+2

        if left < n and arrayValues[i] < arrayValues[left]:
            largest = left

        if right < n and arrayValues[largest] < arrayValues[right]:
            largest = right

        if largest != i:
            arrayValues[i], arrayValues[largest] = arrayValues[largest], arrayValues[i]
            heapify(n, largest)


    def heapSort():
        n = len(arrayValues)

        for i in range(n-1, -1, -1):
            heapify(n, i)

        for i in range(n-1, 0, -1):
            arrayValues[i], arrayValues[0] = arrayValues[0], arrayValues[i]
            heapify(i, 0)
            dynamicDraw([RED if x == i else BLUE for x in range(n)])
            time.sleep(playbackSpeed/len(arrayValues))
        
        dynamicDraw([BLUE for x in range(len(arrayValues))])

    #Merge sort
    def merge(start, middle, end):
        p = start
        q = middle + 1
        tempArray = []

        for i in range(start, end + 1):
            if p > middle:
                tempArray.append(arrayValues[q])
                q += 1
            elif q > end:
                tempArray.append(arrayValues[p])
                p += 1
            elif arrayValues[p] < arrayValues[q]:
                tempArray.append(arrayValues[p])
                p += 1
            else:
                tempArray.append(arrayValues[q])
                q += 1

        for p in range(len(tempArray)):
            arrayValues[start] = tempArray[p]
            start += 1

    def mergeSort(start, end):
        if start < end:
            middle = int((start + end) / 2)
            mergeSort(start, middle)
            mergeSort(middle + 1, end)

            merge(start, middle, end)

            dynamicDraw([DARKESTBLUE if x >= start and x < middle else RED if x == middle else DARKBLUE if x > middle and x <=end else BLUE for x in range(len(arrayValues))])
            time.sleep(playbackSpeed/len(arrayValues))

        dynamicDraw([BLUE for x in range(len(arrayValues))])

    #Quick sort
    def partition(start, end):
        i = start + 1
        pivot = arrayValues[start]

        for j in range(start + 1, end + 1):
            if arrayValues[j] < pivot:
                arrayValues[i], arrayValues[j] = arrayValues[j], arrayValues[i]
                i += 1
        arrayValues[start], arrayValues[i - 1] = arrayValues[i - 1], arrayValues[start]
        return i - 1

    def quickSort(start, end):
        if start < end:
            pivotPosition = partition(start, end)
            quickSort(start, pivotPosition - 1)
            quickSort(pivotPosition + 1, end)
            dynamicDraw([DARKESTBLUE if x >= start and x < pivotPosition else RED if x == pivotPosition else DARKBLUE if x > pivotPosition and x <=end else BLUE for x in range(len(arrayValues))])
            time.sleep(playbackSpeed/len(arrayValues))
            
        dynamicDraw([BLUE for x in range(len(arrayValues))])    

    #Bubble sort
    def bubbleSort():
        for i in range(len(arrayValues)):
            for j in range(0, len(arrayValues) - i - 1):
                if arrayValues[j] > arrayValues[j + 1]:
                    arrayValues[j], arrayValues[j + 1] = arrayValues[j + 1], arrayValues[j]
                    dynamicDraw([RED if x == j or x == j + 1 else BLUE for x in range(len(arrayValues))])

        dynamicDraw([BLUE for x in range(len(arrayValues))])


    root.mainloop()

if __name__ == '__main__':
    main()