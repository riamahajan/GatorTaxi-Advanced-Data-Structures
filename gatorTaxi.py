from collections import deque
import sys
import re


class minHeap:
    def __init__(self) -> None:
        # Initialize instance variables for the heap
        self.size = 0      # Keep track of the number of elements in the heap
        self.Heap = []     # Create an empty list to represent the heap
        self.indmap = {}   # Create an empty dictionary to map elements to their index in the heap

    def insert(self, rideNumber, rideCost, tripDuration, rbnode):
        # Append the ride to the end of the heap list as a new list containing the ride details
        self.Heap.append([rideNumber, rideCost, tripDuration, rbnode])

        # Get the index of the newly added ride in the heap list
        i = len(self.Heap) - 1

        # Update the index mapping of the ride to the newly added index in the heap list
        self.indmap[rbnode] = i

        # Move the newly added ride up the heap to maintain the heap property
        self.upHeapify(i)

        # Return from the function
        return

    def update(self, updatenode, newtripDuration):
        # Get the index of the ride to be updated in the heap list
        IDX = self.indmap[updatenode]

    # Determine the action to take based on the new trip duration
        if newtripDuration <= self.Heap[IDX][2]:
            # If the new trip duration is less than or equal to the current trip duration of the ride:
            # - Update the trip duration of the ride in the heap list
            # - Move the updated ride up the heap to maintain the heap property
            # - Move the updated ride down the heap to maintain the heap property
            self.Heap[IDX][2] = newtripDuration
            self.upHeapify(IDX)
            newind = self.indmap[updatenode]
            self.downHeapify(newind)

        elif self.Heap[IDX][2] < newtripDuration <= 2 * self.Heap[IDX][2]:
            # If the new trip duration is between the current trip duration and twice the current trip duration of the ride:
            # - Increase the ride cost by 10
            # - Update the trip duration of the ride in the heap list
            # - Move the updated ride up the heap to maintain the heap property
            # - Move the updated ride down the heap to maintain the heap property
            self.Heap[IDX][1] += 10
            self.Heap[IDX][2] = newtripDuration
            self.upHeapify(IDX)
            newind = self.indmap[updatenode]
            self.downHeapify(newind)

        elif newtripDuration > 2 * self.Heap[IDX][2]:
            # If the new trip duration is more than twice the current trip duration of the ride:
            # - Cancel the ride
            self.cancel(updatenode)

    def cancel(self, currentNode):
        # Get the index of the ride to be cancelled in the heap list
        IDX = self.indmap[currentNode]

        # Check if the ride to be cancelled is in the heap
        if IDX == -1:
            return

        # If the ride to be cancelled is not the last element in the heap:
        if IDX != len(self.Heap) - 1:
            # Update the index mapping of the last ride in the heap to the index of the ride to be cancelled
            self.indmap[self.Heap[-1][3]] = self.indmap[self.Heap[IDX][3]]

            # Replace the ride to be cancelled with the last ride in the heap
            self.Heap[IDX] = self.Heap.pop()

            # Move the replaced ride down the heap to maintain the heap property
            self.downHeapify(IDX)

        else:
            # If the ride to be cancelled is the last element in the heap:
            # - Delete the ride from the index mapping
            # - Remove the ride from the heap
            del self.indmap[self.Heap[IDX][3]]
            self.Heap.pop()

    def upHeapify(self, i):
        # Check if the ride to be moved up is the root of the heap, or if its cost and trip duration are greater than or equal to its parent's
        if i == 0 or (
            self.Heap[i][1] >= self.Heap[(i - 1) // 2][1]
            and self.Heap[i][2] >= self.Heap[(i - 1) // 2][2]
        ):
            return

        # Otherwise, swap the ride with its parent in the heap list
        self.Heap[i], self.Heap[(i - 1) // 2] = (
            self.Heap[(i - 1) // 2],
            self.Heap[i],
        )

        # Update the index mapping of the rides in the index mapping dictionary
        self.indmap[self.Heap[i][3]], self.indmap[self.Heap[(i - 1) // 2][3]] = (
            self.indmap[self.Heap[(i - 1) // 2][3]],
            self.indmap[self.Heap[i][3]],
        )

        # Recursively move the swapped ride and its parents up the heap to maintain the heap property
        self.upHeapify((i - 1) // 2)

    def GetNextRide(self):
        # Check if the heap is empty
        if not self.Heap:
            return

        # Get the first ride in the heap as the next ride to take
        ans = self.Heap[0]

        # Delete the ride from the index mapping
        del self.indmap[ans[3]]

        # If there is only one ride in the heap:
        if len(self.Heap) == 1:
            # Remove the ride from the heap
            self.Heap.pop()

        # If there is more than one ride in the heap:
        else:
            # Replace the first ride with the last ride in the heap
            self.Heap[0] = self.Heap.pop()

            # Update the index mapping of the last ride in the heap
            self.indmap[self.Heap[0][3]] = 0

            # Move the replaced ride down the heap to maintain the heap property
            self.downHeapify(0)

        # Return the next ride to take
        return ans

    def downHeapify(self, i):
        # Initialize the largest index as the index of the ride itself
        largest = i

        # Check if the left child exists and its cost or trip duration is less than that of the ride:
        left = 2 * i + 1
        if left < len(self.Heap) and (
            (self.Heap[left][1] < self.Heap[largest][1])
            or (
                self.Heap[left][1] == self.Heap[largest][1]
                and self.Heap[left][2] < self.Heap[largest][2]
            )
        ):
            largest = left

        # Check if the right child exists and its cost or trip duration is less than that of the largest child seen so far:
        right = 2 * i + 2
        if right < len(self.Heap) and (
            (self.Heap[right][1] < self.Heap[largest][1])
            or (
                self.Heap[right][1] == self.Heap[largest][1]
                and self.Heap[right][2] < self.Heap[largest][2]
            )
        ):
            largest = right

        # If the largest index is not the index of the original ride:
        if largest != i:
            # Swap the ride with the largest child in the heap list
            self.Heap[i], self.Heap[largest] = self.Heap[largest], self.Heap[i]

            # Update the index mapping of the rides in the index mapping dictionary
            self.indmap[self.Heap[i][3]], self.indmap[self.Heap[largest][3]] = (
                self.indmap[self.Heap[largest][3]],
                self.indmap[self.Heap[i][3]],
            )

            # Recursively move the swapped ride and its children down the heap to maintain the heap property
            self.downHeapify(largest)

        # Return from the function
        return

class Node:
    def __init__(self, rideNumber, rideCost, tripDuration, parent=None, color=1, left=None, right=None):
        """
        Initializes Node object with the specified ride number, cost, and trip duration, along with oparent, color, left child, and right child nodes.

        """
        self.rideNumber = rideNumber  # ride_number (int): The number of the ride.
        self.rideCost = rideCost  # ride_cost (float): The cost of the ride.
        # trip_duration (float): The duration of the ride.
        self.tripDuration = tripDuration
        # parent (RideNode, optional): The parent node. Defaults to None.
        self.parent = parent
        self.color = 1  # default color of node is red
        # left (RideNode, optional): The left child node. Defaults to None.
        self.left = left
        # right (RideNode, optional): The right child node. Defaults to None.
        self.right = right

    def __repr__(self) -> str:
        """
        Returns a string representation of the color of the Node object. 
        """
        # Check the color of the node and return the corresponding string representation
        if self.color == 0:
            return "(b)"      # node is black
        elif self.color == 1:
            return "(r)"      # node is red
        else:
            return "(unknown)"  # node color is unknown


class RedBlackTree:
    def __init__(self):
        # Create a temporary NIL node with arbitrary values
        nil_node = Node(-7, -7, -7)

        # Set color, left, and right attributes for the NIL node
        nil_node.color = 0
        nil_node.left = None
        nil_node.right = None

        # Assign the temporary NIL node to the class attribute 'self.NIL'
        self.NIL = nil_node

        # Set the root of the Red-Black Tree to be the NIL node
        self.root = self.NIL

    def insert(self, rideNumber, rideCost, tripDuration):
        # Search for the ride with the given rideNumber
        existing_node = self.search(rideNumber)

        # If the ride already exists, return NIL
        if existing_node != self.NIL:
            return self.NIL

        # Create a new node with the provided values
        new_node = Node(rideNumber, rideCost, tripDuration)
        new_node.left, new_node.right = self.NIL, self.NIL

        # Initialize temporary variables
        parent_node, current_node = None, self.root

        # Traverse the tree to find the correct position for the new node
        while current_node != self.NIL:
            parent_node = current_node
            if new_node.rideNumber < current_node.rideNumber:
                current_node = current_node.left
            else:
                current_node = current_node.right

        # Assign the parent node and update the tree
        new_node.parent = parent_node

        if parent_node is None:
            self.root = new_node
        elif new_node.rideNumber < parent_node.rideNumber:
            parent_node.left = new_node
        else:
            parent_node.right = new_node

        # Fix any violations in the tree
        self.insert_fix(new_node)

        return new_node

    def insert_fix(self, new_node):
        # Continue while new_node has a parent and its color is red
        while new_node.parent and new_node.parent.color == 1:
            if new_node.parent == new_node.parent.parent.left:
                uncle_node = new_node.parent.parent.right

                # Case 1: Uncle node is red
                if uncle_node.color == 1:
                    new_node.parent.color = 0
                    uncle_node.color = 0
                    new_node.parent.parent.color = 1
                    new_node = new_node.parent.parent
                else:
                    # Case 2: New node is a right child
                    if new_node == new_node.parent.right:
                        new_node = new_node.parent
                        self.rotate_left(new_node)

                    # Case 3: New node is a left child
                    new_node.parent.color = 0
                    new_node.parent.parent.color = 1
                    self.rotate_right(new_node.parent.parent)
            else:
                uncle_node = new_node.parent.parent.left

                # Case 1: Uncle node is red
                if uncle_node.color == 1:
                    new_node.parent.color = 0
                    uncle_node.color = 0
                    new_node.parent.parent.color = 1
                    new_node = new_node.parent.parent
                else:
                    # Case 2: New node is a left child
                    if new_node == new_node.parent.left:
                        new_node = new_node.parent
                        self.rotate_right(new_node)

                    # Case 3: New node is a right child
                    new_node.parent.color = 0
                    new_node.parent.parent.color = 1
                    self.rotate_left(new_node.parent.parent)

            # Stop when new_node reaches the root
            if new_node == self.root:
                break

        # Set the root color to black
        self.root.color = 0

    def rotate_left(self, currNode):
        # Save the right child of the current node as 'temp'
        temp = currNode.right

        # Update the parent of temp's left child to be currNode
        if temp.left != self.NIL:
            temp.left.parent = currNode

        # Set the right child of currNode to be the left child of temp
        currNode.right = temp.left

        # Update the parent of temp to be currNode's parent
        temp.parent = currNode.parent

        # Update the parent of the root node (if currNode is the root)
        # or the appropriate child of the parent to be temp
        if currNode.parent is None:
            self.root = temp
        elif currNode == currNode.parent.left:
            currNode.parent.left = temp
        else:
            currNode.parent.right = temp

        # Set the left child of temp to be currNode, and update currNode's parent to be temp
        temp.left = currNode
        currNode.parent = temp

    def rotate_right(self, currNode):
        # Save the left child of the current node as 'temp'
        temp = currNode.left

        # Update the parent of temp's right child to be currNode
        if temp.right != self.NIL:
            temp.right.parent = currNode

        # Set the left child of currNode to be the right child of temp
        currNode.left = temp.right

        # Update the parent of temp to be currNode's parent
        temp.parent = currNode.parent

        # Update the parent of the root node (if currNode is the root)
        # or the appropriate child of the parent to be temp
        if currNode.parent is None:
            self.root = temp
        elif currNode == currNode.parent.right:
            currNode.parent.right = temp
        else:
            currNode.parent.left = temp

        # Set the right child of temp to be currNode, and update currNode's parent to be temp
        temp.right = currNode
        currNode.parent = temp

    # Delete a node from the tree
    def delete(self, currentNode):
        if currentNode == self.NIL:   # Check if node is empty
            return

        tempNode = currentNode
        temp = currentNode
        yoc = tempNode.color

        # Case 1: Node has only a right child
        if currentNode.left == self.NIL:
            x = currentNode.right
            self.replace(currentNode, currentNode.right)

        # Case 2: Node has only a left child
        elif currentNode.right == self.NIL:
            x = currentNode.left
            self.replace(currentNode, currentNode.left)

        # Case 3: Node has two children
        else:
            # Get the minimum value in the right subtree
            tempNode = self.minimum(currentNode.right)
            yoc = tempNode.color   # Save the color of the successor node
            x = tempNode.right

            if tempNode.parent == currentNode:
                x.parent = tempNode
            else:
                # Replace the successor with its right child
                self.replace(tempNode, tempNode.right)
                tempNode.right = currentNode.right
                tempNode.right.parent = tempNode

            # Replace the node with its successor
            self.replace(currentNode, tempNode)
            tempNode.left = currentNode.left
            tempNode.left.parent = tempNode
            tempNode.color = currentNode.color

        # Fix the tree if the removed node was black
        if yoc == 0:
            self.delete_fix(x)

        return temp

    # Fix the red-black tree violations after node deletion

    def delete_fix(self, fix):
        # Fix until the root or a red node is reached
        while fix != self.root and fix.color == 0:
            if fix == fix.parent.left:   # Fix for the left child of the parent
                sibling = fix.parent.right   # Get the sibling of the node

                # Case 1: The sibling is red
                if sibling.color == 1:
                    sibling.color = 0
                    fix.parent.color = 1
                    self.rotate_left(fix.parent)   # Left rotate the parent
                    sibling = fix.parent.right   # Update the sibling

                # Case 2: The sibling is black and both its children are black
                if sibling.left.color == 0 and sibling.right.color == 0:
                    sibling.color = 1   # Color the sibling red
                    fix = fix.parent   # Move up to the parent

                # Case 3: The sibling is black and its left child is red and right child is black
                else:
                    if sibling.right.color == 0:
                        sibling.left.color = 0
                        sibling.color = 1
                        # Right rotate the sibling's left child
                        self.rotate_right(sibling)
                        sibling = fix.parent.right   # Update the sibling

                    # Case 4: The sibling is black and its right child is red
                    sibling.color = fix.parent.color
                    fix.parent.color = 0
                    sibling.right.color = 0
                    self.rotate_left(fix.parent)   # Left rotate the parent
                    fix = self.root   # Fix completed, move up to the root node
            else:   # Fix for the right child of the parent
                sibling = fix.parent.left   # Get the sibling of the node

                # Case 1: The sibling is red
                if sibling.color == 1:
                    sibling.color = 0
                    fix.parent.color = 1
                    self.rotate_right(fix.parent)   # Right rotate the parent
                    sibling = fix.parent.left   # Update the sibling

                # Case 2: The sibling is black and both its children are black
                if sibling.right.color == 0 and sibling.left.color == 0:
                    sibling.color = 1   # Color the sibling red
                    fix = fix.parent   # Move up to the parent

                # Case 3: The sibling is black and its right child is red and left child is black
                else:
                    if sibling.left.color == 0:
                        sibling.right.color = 0
                        sibling.color = 1
                        # Left rotate the sibling's right child
                        self.rotate_left(sibling)
                        sibling = fix.parent.left   # Update the sibling

                    # Case 4: The sibling is black and its left child is red
                    sibling.color = fix.parent.color
                    fix.parent.color = 0
                    sibling.left.color = 0
                    self.rotate_right(fix.parent)   # Right rotate the parent
                    fix = self.root   # Fix completed, move up to the root node
        fix.color = 0   # Set the color of the node to black

    # Replace one node with another in the tree

    def replace(self, u, v):
        # If u is the root node
        if u.parent is None:
            # Set v as the new root node
            self.root = v
        # If u is the left child of its parent
        elif u == u.parent.left:
            # Set v as the new left child of u's parent
            u.parent.left = v
        # If u is the right child of its parent
        else:
            # Set v as the new right child of u's parent
            u.parent.right = v

        # If v is not None (i.e., it exists)
        if v is not None:
            # Update the parent of v to be the parent of u
            v.parent = u.parent

    # Find the minimum node in the subtree rooted at the target node

    def minimum(self, target):
        while target.left != self.NIL:
            target = target.left   # Traverse down the left subtree until the minimum node is found
        return target   # Return the minimum node

    # Search for a node with the given ride number in the tree

    def search(self, rideNumberval):
        currentNode = self.root   # Start at the root node
        # Traverse down the tree until the ride number is found or the current node is nil
        while currentNode != self.NIL and rideNumberval != currentNode.rideNumber:
            if rideNumberval < currentNode.rideNumber:
                # If the ride number is less than the current node's ride number, move to the left child
                currentNode = currentNode.left
            else:
                # If the ride number is greater than the current node's ride number, move to the right child
                currentNode = currentNode.right
        return currentNode   # Return the node with the given ride number or nil if it is not found

    def Print(self, start_ride, end_ride):
        rides = []
        # Collect rides within the given range (start_ride, end_ride)
        self.collect_rides(rides, self.root, start_ride, end_ride)
        return rides

    def collect_rides(self, rides_list, node, start_ride, end_ride):
        if node == self.NIL:
            return

        # Traverse left subtree if the current node's ride number is greater than the start_ride
        if start_ride < node.rideNumber:
            self.collect_rides(rides_list, node.left, start_ride, end_ride)

        # If the current node's ride number is within the range, add the ride details to the rides_list
        if start_ride <= node.rideNumber <= end_ride:
            rides_list.append(
                (node.rideNumber, node.rideCost, node.tripDuration))

        # Traverse right subtree if the current node's ride number is less than the end_ride
        if node.rideNumber < end_ride:
            self.collect_rides(rides_list, node.right, start_ride, end_ride)

    # Update the trip duration and ride cost of a node in the tree

    def update(self, node, new_duration):
        # If the new duration is less than or equal to the current duration
        if new_duration <= node.tripDuration:
            node.tripDuration = new_duration
        # If the new duration is greater than twice the current duration
        elif new_duration > 2 * node.tripDuration:
            self.delete(node)  # Delete the node from the tree
        # Otherwise (the new duration is between the current duration and twice the current duration)
        else:
            node.rideCost += 10  # Increase the ride cost by 10
            node.tripDuration = new_duration  # Update the trip duration

    # Print the ride numbers of all nodes in the tree using level-order traversal


    def print_tree(self, print_color=True):
        # Initialize the queue with the root node
        queue = [self.root]

        # Traverse the tree in level-order
        for node in queue:
            # Print the ride number of the current node
            if print_color:
                print(f"{node.rideNumber}{node.print_color()}", end=" ")
            else:
                print(node.rideNumber, end=" ")

            # Add the left and right child nodes of the current node to the queue
            if node.left != self.NIL:
                queue.append(node.left)
            if node.right != self.NIL:
                queue.append(node.right)

            # Remove the first node from the queue
            queue.pop(0)

            # Break the loop if the queue is empty
            if not queue:
                break


class Gatortaxi:

    def __init__(self):
        self.rbt = RedBlackTree()
        self.heap = minHeap()

    def run(self, input_file, output_file):
        with open(input_file, "r") as f, open(output_file, "w") as o:
            for line in f:
                args = re.findall("\((.*?)\)", line)
                if "Insert" in line:
                    rideNumber, rideCost, tripDuration = [
                        int(arg) if arg.isdigit() else arg for arg in args[0].split(",")
                    ]
                    currentNode = self.rbt.insert(rideNumber, rideCost, tripDuration)
                    if currentNode == self.rbt.NIL:
                        o.write("Duplicate RideNumber" + "\n")
                        break
                    else:
                        self.heap.insert(rideNumber, rideCost, tripDuration, currentNode)
                elif "GetNextRide" in line:
                    nextRide = self.heap.GetNextRide()
                    if nextRide:
                        self.rbt.delete(nextRide[3])
                        o.write(str((nextRide[0], nextRide[1], nextRide[2])) + "\n")
                    else:
                        o.write("No active Ride Requests\n")
                elif "UpdateTrip" in line:
                    rideNumber, newtripDuration = [
                        int(arg) if arg.isdigit() else arg for arg in args[0].split(",")
                    ]
                    updatenode = self.rbt.search(rideNumber)
                    self.heap.update(updatenode, newtripDuration)
                    self.rbt.update(updatenode, newtripDuration)
                elif "CancelRide" in line:
                    rideNumber = int(args[0])
                    delnode = self.rbt.search(rideNumber)
                    if delnode != self.rbt.NIL:
                        self.heap.cancel(delnode)
                        self.rbt.delete(delnode)
                elif "Print" in line:
                    printargs = [
                        int(arg) if arg.isdigit() else arg for arg in args[0].split(",")
                    ]
                    if len(printargs) == 1:
                        currentNode = self.rbt.search(printargs[0])
                        if currentNode == self.rbt.NIL:
                            o.write("(0, 0, 0)\n")
                        else:
                            o.write(
                                str((currentNode.rideNumber, currentNode.rideCost,
                                    currentNode.tripDuration)) + "\n"
                            )
                    else:
                        nodes = self.rbt.Print(printargs[0], printargs[1])
                        if len(nodes) == 0:
                            o.write("(0, 0, 0)\n")

                        else:
                            outline = ",".join(str(currentNode)
                                               for currentNode in nodes)
                            o.write(outline + "\n")

def main():
    if len(sys.argv) != 2:
        print("Usage: python gatorTaxi.py input.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = "output.txt"

    gatortaxi = Gatortaxi()
    gatortaxi.run(input_file, output_file)


if __name__ == "__main__":
    main()
