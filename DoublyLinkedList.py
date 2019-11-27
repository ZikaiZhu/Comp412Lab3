from collections import defaultdict

from DependenceGraph import DependenceGraph

reversed_dict = {0 : "load", 1 : "store", 2 : "loadI", 3 : "add", 4 : "sub", 5 : "mult", 6 : "lshift", 7 : "rshift", 8 : "output", 9 : "nop", 10 : "constant", 11 : "register", 12 : "comma", 13 : "into"}
op_to_weight = {0 : 5, 1 : 5, 2 : 1, 3 : 1, 4 : 1, 5 : 3, 6 : 1, 7 : 1, 8 : 1, 9 : 1}
class DoublyLinkedList:
    def __init__(self):
        self.prev = None
        self.next = None
        self.opcode = None
        self.first_operand = ["empty", "empty", "empty", "empty"]
        self.second_operand = ["empty", "empty", "empty", "empty"]
        self.third_operand = ["empty", "empty", "empty", "empty"]
        self.index = None
        self.max_live = -float("inf")
        self.location_code = 32768

    def set_next(self, next_node):
        self.next = next_node
        next_node.prev = self

    def set_prev(self, prev_node):
        self.prev = prev_node
        prev_node.next = self

    def set_memop(self, opcode, reg1, reg2):
        self.opcode = opcode
        self.first_operand[0] = reg1
        self.third_operand[0] = reg2

    def set_loadI(self, opcode, reg1, constant):
        self.opcode = opcode
        self.first_operand[0] = constant
        self.third_operand[0] = reg1

    def set_arithop(self, opcode, reg1, reg2, reg3):
        self.opcode = opcode
        self.first_operand[0] = reg1
        self.second_operand[0] = reg2
        self.third_operand[0] = reg3

    def set_output(self, opcode, constant):
        self.opcode = opcode
        self.first_operand[0] = constant

    def set_nop(self, opcode):
        self.opcode = opcode

    def get_prev(self):
        return self.prev

    def get_next(self):
        return self.next

    def get_opcode(self):
        return self.opcode

    def get_firstOperand(self):
        return self.first_operand

    def get_secondOperand(self):
        return self.second_operand

    def get_thirdOperand(self):
        return self.third_operand

    def set_and_return_index_tail(self):
        index = 0
        cur = self
        while cur.next:
            cur.index = index
            index += 1
            cur = cur.next
        cur.index = index
        return index, cur

    def get_index(self):
        return self.index

    def get_max_register(self):
        maxi = 0
        cur = self
        while cur.next:
            if cur.first_operand[0] != "empty":
                if cur.first_operand[0][0] == "r":
                    first_num = int(cur.first_operand[0][1:])
                    if first_num > maxi:
                        maxi = first_num
            if cur.second_operand[0] != "empty":
                if cur.second_operand[0][0] == "r":
                    second_num = int(cur.second_operand[0][1:])
                    if second_num > maxi:
                        maxi = second_num
            if cur.third_operand[0] != "empty":
                if cur.third_operand[0][0] == "r":
                    third_num = int(cur.third_operand[0][1:])
                    if third_num > maxi:
                        maxi = third_num
            cur = cur.next
        return maxi

    def get_max_renamed(self):
        maxi = 0
        cur = self
        while cur.next:
            if cur.first_operand[0] != "empty":
                if cur.first_operand[1][0] == "r":
                    first_num = int(cur.first_operand[1][1:])
                    if first_num > maxi:
                        maxi = first_num
            if cur.second_operand[0] != "empty":
                if cur.second_operand[1][0] == "r":
                    second_num = int(cur.second_operand[1][1:])
                    if second_num > maxi:
                        maxi = second_num
            if cur.third_operand[0] != "empty":
                if cur.third_operand[1][0] == "r":
                    third_num = int(cur.third_operand[1][1:])
                    if third_num > maxi:
                        maxi = third_num
            cur = cur.next
        return maxi

    def build_dependence_graph(self):
        m_map = defaultdict(DependenceGraph)
        index_map = {}
        edge_list = set()
        cur = self
        while cur:
            #print (cur.get_firstOperand()[1], cur.get_secondOperand()[1], cur.get_thirdOperand()[1])
            # case for store
            if cur.get_opcode() == 1:
                cur_Node = DependenceGraph()
                cur_Node.set_opindex(cur.get_index())
                cur_Node.set_operation(cur)
                used_vr1 = cur.get_firstOperand()[1]
                used_vr2 = cur.get_thirdOperand()[1]
                used_node1 = m_map[used_vr1]
                used_node2 = m_map[used_vr2]
                if used_node1:
                    if used_node1.get_opindex() != None:
                        cur_Node.add_next(used_node1)
                        used_node1.add_parent(cur_Node)
                        cur_weight = op_to_weight[used_node1.get_operation().get_opcode()]
                        cur_Node.set_edge_weights(used_node1, cur_weight)
                        edge_list.add((cur_Node, used_node1, cur_weight))
                if used_node2:
                    if used_node2.get_opindex() != None:
                        cur_Node.add_next(used_node2)
                        used_node2.add_parent(cur_Node)
                        cur_weight = op_to_weight[used_node2.get_operation().get_opcode()]
                        cur_Node.set_edge_weights(used_node2, cur_weight)
                        edge_list.add((cur_Node, used_node2, cur_weight))
                # now find the most recent store
                store_iter = cur.prev
                while store_iter:
                    if store_iter.get_opcode() == 1:
                        store_node = index_map[store_iter.get_index()]
                        cur_Node.add_next(store_node)
                        store_node.add_parent(cur_Node)
                        cur_Node.set_edge_weights(store_node, 1)
                        if (cur_Node, store_node, 5) not in edge_list:
                            edge_list.add((cur_Node, store_node, 1))
                        break
                    store_iter = store_iter.prev
                #now find all prev load & output
                load_output_iter = cur.prev
                while load_output_iter:
                    if load_output_iter.get_opcode() == 0 or load_output_iter.get_opcode() == 8:
                        lop_node = index_map[load_output_iter.get_index()]
                        cur_Node.add_next(lop_node)
                        lop_node.add_parent(cur_Node)
                        cur_Node.set_edge_weights(lop_node, 1)
                        if (cur_Node, lop_node, 5) not in edge_list:
                            edge_list.add((cur_Node, lop_node, 1))
                    load_output_iter = load_output_iter.prev
                index_map[cur.get_index()] = cur_Node
            else:
                cur_Node = DependenceGraph()
                cur_Node.set_opindex(cur.get_index())
                cur_Node.set_operation(cur)
                if cur.get_thirdOperand()[1] != "empty":
                    m_map[cur.get_thirdOperand()[1]] = cur_Node
                index_map[cur.get_index()] = cur_Node
                used_vr1 = cur.get_firstOperand()[1]
                used_vr2 = cur.get_secondOperand()[1]
                used_node1 = m_map[used_vr1]
                used_node2 = m_map[used_vr2]
                if used_node1:
                    if used_node1.get_opindex() != None:
                        cur_Node.add_next(used_node1)
                        used_node1.add_parent(cur_Node)
                        cur_weight = op_to_weight[used_node1.get_operation().get_opcode()]
                        cur_Node.set_edge_weights(used_node1, cur_weight)
                        edge_list.add((cur_Node, used_node1, cur_weight))
                if used_node2:
                    if used_node2.get_opindex() != None:
                        cur_Node.add_next(used_node2)
                        used_node2.add_parent(cur_Node)
                        cur_weight = op_to_weight[used_node2.get_operation().get_opcode()]
                        cur_Node.set_edge_weights(used_node2, cur_weight)
                        edge_list.add((cur_Node, used_node2, cur_weight))
                # case for load and output
                if cur.get_opcode() == 0 or cur.get_opcode() == 8:
                    store_iter = cur.prev
                    while store_iter:
                        if store_iter.get_opcode() == 1:
                            lop_node = index_map[store_iter.get_index()]
                            cur_Node.add_next(lop_node)
                            lop_node.add_parent(cur_Node)
                            cur_weight = op_to_weight[lop_node.get_operation().get_opcode()]
                            cur_Node.set_edge_weights(lop_node, cur_weight)
                            edge_list.add((cur_Node, lop_node, cur_weight))
                            break
                        store_iter = store_iter.prev
                # case for output
                if cur.get_opcode() == 8:
                    output_iter = cur.prev
                    while output_iter:
                        #print (output_iter.get_index(), output_iter.get_opcode())
                        if output_iter.get_opcode() == 8:
                            lop_node = index_map[output_iter.get_index()]
                            cur_Node.add_next(lop_node)
                            lop_node.add_parent(cur_Node)
                            cur_Node.set_edge_weights(lop_node, 1)
                            edge_list.add((cur_Node, lop_node, 1))
                            break
                        output_iter = output_iter.prev
                if not cur_Node.get_next():
                    edge_list.add((cur_Node, None))
            cur = cur.next
        distinct_nodes = set()
        for edge in edge_list:
            distinct_nodes.add(edge[0])
            if edge[1]:
                distinct_nodes.add(edge[1])
        for dist in distinct_nodes:
            if not dist.get_parent():
                dist.set_prio_from_root()
        return edge_list

    def print_operation(self):
        strres = ""
        strres += reversed_dict[self.get_opcode()]
        strres += " "
        if self.get_firstOperand()[1] != "empty":
            strres += self.get_firstOperand()[1]
        else:
            if self.get_firstOperand()[0] != "empty":
                strres += self.get_firstOperand()[0]
        if self.get_secondOperand()[0] != "empty":
            strres += ", "
            strres += self.get_secondOperand()[1]
        if self.get_thirdOperand()[0] != "empty":
            strres += " => "
            strres += self.get_thirdOperand()[1]
        if strres[-1] == " ":
            return strres[:-1]
        return strres





    def rename_algorithm(self):
        index, tail = self.set_and_return_index_tail()
        vr_name = 0
        max_sr_num = self.get_max_register()
        sr_to_vr = ["invalid"] * (max_sr_num + 1)
        lu = [float("inf")] * (max_sr_num + 1)
        live_count = 0
        max_live = -float("inf")
        cur = tail
        while cur.get_opcode() != None:
            if cur.get_opcode() == 1:
                firstop = cur.get_firstOperand()
                thirdop = cur.get_thirdOperand()
                firstsr = int(firstop[0][1:])
                thirdsr = int(thirdop[0][1:])
                if sr_to_vr[firstsr] == "invalid":
                    live_count += 1
                    max_live = max(max_live, live_count)
                    sr_to_vr[firstsr] = str(vr_name)
                    vr_name += 1
                cur.get_firstOperand()[1] = "r" + sr_to_vr[firstsr]
                cur.get_firstOperand()[3] = str(lu[firstsr])
                lu[firstsr] = cur.get_index()
                if sr_to_vr[thirdsr] == "invalid":
                    live_count += 1
                    max_live = max(max_live, live_count)
                    sr_to_vr[thirdsr] = str(vr_name)
                    vr_name += 1
                cur.get_thirdOperand()[1] = "r" + sr_to_vr[thirdsr]
                cur.get_thirdOperand()[3] = str(lu[thirdsr])
                lu[thirdsr] = cur.get_index()
                #print(cur.get_thirdOperand())
                cur = cur.prev
            elif cur.get_opcode() == 8 or cur.get_opcode() == 9:
                cur = cur.prev
                continue
            else:
                firstop = cur.get_firstOperand()
                secondop = cur.get_secondOperand()
                thirdop = cur.get_thirdOperand()
                # First to handle the define cases
                third_sr = int(thirdop[0][1:])
                if sr_to_vr[third_sr] == "invalid":
                    live_count += 1
                    max_live = max(max_live, live_count)
                    sr_to_vr[third_sr] = str(vr_name)
                    vr_name += 1
                cur.get_thirdOperand()[1] = "r" + sr_to_vr[third_sr]
                cur.get_thirdOperand()[3] = str(lu[third_sr])
                sr_to_vr[third_sr] = "invalid"
                live_count -= 1
                lu[third_sr] = float("inf")
                # Now to deal with use cases
                if firstop[0][0] == "r":
                    first_sr = int(firstop[0][1:])
                    if sr_to_vr[first_sr] == "invalid":
                        live_count += 1
                        max_live = max(max_live, live_count)
                        sr_to_vr[first_sr] = str(vr_name)
                        vr_name += 1
                    cur.get_firstOperand()[1] = "r" + sr_to_vr[first_sr]
                    cur.get_firstOperand()[3] = str(lu[first_sr])
                    lu[first_sr] = cur.get_index()
                if secondop[0] != "empty":
                    second_sr = int(secondop[0][1:])
                    if sr_to_vr[second_sr] == "invalid":
                        live_count += 1
                        max_live = max(max_live, live_count)
                        sr_to_vr[second_sr] = str(vr_name)
                        vr_name += 1
                    cur.get_secondOperand()[1] = "r" + sr_to_vr[second_sr]
                    cur.get_secondOperand()[3] = str(lu[second_sr])
                    lu[second_sr] = cur.get_index()
                #print(cur.get_thirdOperand())
                cur = cur.prev
        cur.next.max_live = max_live
        return cur.next


    def allocate_physical(self, k):
        # the case for no spilling
        if self.max_live <= k:
            maxi_renamed = self.get_max_renamed() + 1
            vr_to_pr = ["invalid"] * maxi_renamed
            pr_to_vr = ["invalid"] * k
            pr_nu = [float("inf")] * k
            pr_stack = list(range(0, k))[::-1]
            cur = self
            while cur:
                # the case for store
                if cur.get_opcode() == 1:
                    firstop = cur.get_firstOperand()
                    firstvr = int(firstop[1][1:])
                    first_pr = vr_to_pr[firstvr]
                    first_nu = firstop[3]
                    if first_nu != "empty":
                        if first_nu != "inf":
                            first_nu = int(first_nu)
                        else:
                            first_nu = float("inf")
                    if first_pr == "invalid":
                        first_pr = pr_stack.pop()
                        vr_to_pr[firstvr] = first_pr
                        pr_to_vr[first_pr] = firstvr
                        pr_nu[first_pr] = first_nu
                        firstop[2] = "r" + str(first_pr)
                    else:
                        firstop[2] = "r" + str(first_pr)
                    cur.first_operand = firstop
                    thirdop = cur.get_thirdOperand()
                    thirdvr = int(thirdop[1][1:])
                    third_pr = vr_to_pr[thirdvr]
                    third_nu = thirdop[3]
                    if third_nu != "empty":
                        if third_nu != "inf":
                            third_nu = int(third_nu)
                        else:
                            third_nu = float("inf")
                    if third_pr == "invalid":
                        third_pr = pr_stack.pop()
                        vr_to_pr[thirdvr] = third_pr
                        pr_to_vr[third_pr] = thirdvr
                        pr_nu[third_pr] = third_nu
                        thirdop[2] = "r" + str(third_pr)
                    else:
                        thirdop[2] = "r" + str(third_pr)
                    cur.third_operand = thirdop
                    if first_nu == float("inf") and first_pr != "invalid":
                        vr_to_pr[pr_to_vr[first_pr]] = "invalid"
                        pr_to_vr[first_pr] = "invalid"
                        pr_nu[first_pr] = float("inf")
                        pr_stack.append(first_pr)
                    if third_nu == float("inf") and third_pr != "invalid":
                        vr_to_pr[pr_to_vr[third_pr]] = "invalid"
                        pr_to_vr[third_pr] = "invalid"
                        pr_nu[third_pr] = float("inf")
                        pr_stack.append(third_pr)
                    res = ""
                    res += reversed_dict[cur.get_opcode()]
                    res += " "
                    res += firstop[2]
                    res += " => "
                    res += thirdop[2]
                    print (res)
                    cur = cur.next
                elif cur.get_opcode() == 8 or cur.get_opcode() == 9:
                    res = ""
                    res += reversed_dict[cur.get_opcode()]
                    res += " "
                    if cur.get_firstOperand()[1] != "empty":
                        res += cur.get_firstOperand()[1]
                    else:
                        if cur.get_firstOperand()[0] != "empty":
                            res += cur.get_firstOperand()[0]
                    if cur.get_secondOperand()[0] != "empty":
                        res += ", "
                        res += cur.get_secondOperand()[1]
                    if cur.get_thirdOperand()[0] != "empty":
                        res += " => "
                        res += cur.get_thirdOperand()[1]
                    print(res)
                    cur = cur.next
                    continue
                else:
                    firstop = cur.get_firstOperand()
                    secondop = cur.get_secondOperand()
                    thirdop = cur.get_thirdOperand()
                    # First to deal with use cases and first op
                    first_nu = firstop[3]
                    if first_nu != "empty":
                        if first_nu != "inf":
                            first_nu = int(first_nu)
                        else:
                            first_nu = float("inf")
                    else:
                        first_nu = float("inf")
                    if firstop[1][0] == "r":
                        firstvr = int(firstop[1][1:])
                        first_pr = vr_to_pr[firstvr]
                        if first_pr == "invalid":
                            first_pr = pr_stack.pop()
                            vr_to_pr[firstvr] = first_pr
                            pr_to_vr[first_pr] = firstvr
                            pr_nu[firstvr] = first_nu
                            firstop[2] = "r" + str(first_pr)
                        else:
                            firstop[2] = "r" + str(first_pr)
                    cur.first_operand = firstop
                    # Secondly to deal with the use case and second op
                    second_nu = secondop[3]
                    if second_nu != "empty":
                        if second_nu != "inf":
                            second_nu = int(second_nu)
                        else:
                            second_nu = float("inf")
                    else:
                        second_nu = float("inf")
                    if secondop[0] != "empty":
                        if secondop[1][0] == "r":
                            secondvr = int(secondop[1][1:])
                            second_pr = vr_to_pr[secondvr]
                            if second_pr == "invalid":
                                second_pr = pr_stack.pop()
                                vr_to_pr[secondvr] = second_pr
                                pr_to_vr[second_pr] = secondvr
                                pr_nu[second_pr] = second_nu
                                secondop[2] = "r" + str(second_pr)
                            else:
                                secondop[2] = "r" + str(second_pr)
                    cur.second_operand = secondop
                    if second_nu == float("inf") and secondop[2] != "empty":
                        vr_to_pr[pr_to_vr[second_pr]] = "invalid"
                        pr_to_vr[second_pr] = "invalid"
                        pr_nu[second_pr] = float("inf")
                        pr_stack.append(second_pr)
                    if first_nu == float("inf") and firstop[2] != "empty":
                        vr_to_pr[pr_to_vr[first_pr]] = "invalid"
                        pr_to_vr[first_pr] = "invalid"
                        pr_nu[first_pr] = float("inf")
                        pr_stack.append(first_pr)
                    # Now to handle the define cases
                    if thirdop[1][0] == "r":
                        third_nu = thirdop[3]
                        if third_nu != "empty":
                            if third_nu != "inf":
                                third_nu = int(third_nu)
                            else:
                                third_nu = float("inf")
                        else:
                            third_nu = float("inf")
                        thirdvr = int(thirdop[1][1:])
                        third_pr = vr_to_pr[thirdvr]
                        thirdvr = int(thirdop[1][1:])
                        third_pr = vr_to_pr[thirdvr]
                        if third_pr == "invalid":
                            third_pr = pr_stack.pop()
                            vr_to_pr[thirdvr] = third_pr
                            pr_to_vr[third_pr] = thirdvr
                            pr_nu[third_pr] = third_nu
                            thirdop[2] = "r" + str(third_pr)
                        else:
                            thirdop[2] = "r" + str(third_pr)
                    cur.third_operand = thirdop
                    res = ""
                    res += reversed_dict[cur.get_opcode()]
                    res += " "
                    if cur.get_firstOperand()[2] != "empty":
                        res += cur.get_firstOperand()[2]
                    else:
                        if cur.get_firstOperand()[0] != "empty":
                            res += cur.get_firstOperand()[0]
                    if cur.get_secondOperand()[0] != "empty":
                        res += ", "
                        res += cur.get_secondOperand()[2]
                    if cur.get_thirdOperand()[0] != "empty":
                        res += " => "
                        res += cur.get_thirdOperand()[2]
                    print(res)
                    cur = cur.next
        else:
            maxi_renamed = self.get_max_renamed() + 1
            vr_to_pr = ["invalid"] * maxi_renamed
            pr_to_vr = ["invalid"] * k
            pr_nu = [float("inf")] * k
            pr_stack = list(range(0, k - 1))[::-1]
            vr_to_spill = defaultdict(int)
            reserved_pr = k - 1
            vr_to_val = defaultdict(int)
            cur = self
            while cur:
                #print (pr_nu)
                # the case for store
                if cur.get_opcode() == 1:
                    marks = []
                    firstop = cur.get_firstOperand()
                    firstvr = int(firstop[1][1:])
                    first_pr = vr_to_pr[firstvr]
                    first_nu = firstop[3]
                    if first_nu != "empty":
                        if first_nu != "inf":
                            first_nu = int(first_nu)
                        else:
                            first_nu = float("inf")
                    if first_pr == "invalid":
                        if firstvr in vr_to_spill:
                            first_pr, pr_nu, vr_to_pr, pr_to_vr, vr_to_spill, pr_stack = self.restore(firstvr, pr_nu, vr_to_pr, pr_to_vr, vr_to_spill, pr_stack, reserved_pr, marks, vr_to_val)
                        elif pr_stack:
                            first_pr = pr_stack.pop()
                        else:
                            first_pr, pr_nu, vr_to_pr, pr_to_vr, vr_to_spill = self.spill(firstvr, pr_nu, vr_to_pr, pr_to_vr, vr_to_spill, reserved_pr, marks, vr_to_val)
                        vr_to_pr[firstvr] = first_pr
                        pr_to_vr[first_pr] = firstvr
                        pr_nu[first_pr] = first_nu
                        firstop[2] = "r" + str(first_pr)
                    else:
                        pr_nu[first_pr] = first_nu
                        firstop[2] = "r" + str(first_pr)
                    cur.first_operand = firstop
                    marks.append(first_pr)
                    thirdop = cur.get_thirdOperand()
                    thirdvr = int(thirdop[1][1:])
                    third_pr = vr_to_pr[thirdvr]
                    third_nu = thirdop[3]
                    if third_nu != "empty":
                        if third_nu != "inf":
                            third_nu = int(third_nu)
                        else:
                            third_nu = float("inf")
                    if third_pr == "invalid":
                        if thirdvr in vr_to_spill:
                            third_pr, pr_nu, vr_to_pr, pr_to_vr, vr_to_spill, pr_stack = self.restore(thirdvr, pr_nu, vr_to_pr, pr_to_vr, vr_to_spill, pr_stack, reserved_pr, marks, vr_to_val)
                        elif pr_stack:
                            third_pr = pr_stack.pop()
                        else:
                            third_pr, pr_nu, vr_to_pr, pr_to_vr, vr_to_spill = self.spill(thirdvr, pr_nu, vr_to_pr, pr_to_vr, vr_to_spill, reserved_pr, marks, vr_to_val)
                        vr_to_pr[thirdvr] = third_pr
                        pr_to_vr[third_pr] = thirdvr
                        pr_nu[third_pr] = third_nu
                        thirdop[2] = "r" + str(third_pr)
                    else:
                        pr_nu[third_pr] = third_nu
                        thirdop[2] = "r" + str(third_pr)
                    cur.third_operand = thirdop
                    marks.append(third_pr)
                    if first_nu == float("inf") and first_pr != "invalid":
                        vr_to_pr[pr_to_vr[first_pr]] = "invalid"
                        pr_to_vr[first_pr] = "invalid"
                        pr_nu[first_pr] = float("inf")
                        pr_stack.append(first_pr)
                    if third_nu == float("inf") and third_pr != "invalid":
                        vr_to_pr[pr_to_vr[third_pr]] = "invalid"
                        pr_to_vr[third_pr] = "invalid"
                        pr_nu[third_pr] = float("inf")
                        pr_stack.append(third_pr)
                    res = ""
                    res += reversed_dict[cur.get_opcode()]
                    res += " "
                    res += firstop[2]
                    res += " => "
                    res += thirdop[2]
                    print (res)
                    cur = cur.next
                # the case for nop and output
                elif cur.get_opcode() == 8 or cur.get_opcode() == 9:
                    res = ""
                    res += reversed_dict[cur.get_opcode()]
                    res += " "
                    if cur.get_firstOperand()[1] != "empty":
                        res += cur.get_firstOperand()[1]
                    else:
                        if cur.get_firstOperand()[0] != "empty":
                            res += cur.get_firstOperand()[0]
                    if cur.get_secondOperand()[0] != "empty":
                        res += ", "
                        res += cur.get_secondOperand()[1]
                    if cur.get_thirdOperand()[0] != "empty":
                        res += " => "
                        res += cur.get_thirdOperand()[1]
                    print(res)
                    cur = cur.next
                    continue
                else:
                    marks = []
                    firstop = cur.get_firstOperand()
                    secondop = cur.get_secondOperand()
                    thirdop = cur.get_thirdOperand()
                    #print (firstop, secondop, thirdop)
                    # First to deal with use cases and first op
                    first_nu = firstop[3]
                    if first_nu != "empty":
                        if first_nu != "inf":
                            first_nu = int(first_nu)
                        else:
                            first_nu = float("inf")
                    else:
                        first_nu = float("inf")
                    if firstop[1][0] == "r":
                        firstvr = int(firstop[1][1:])
                        first_pr = vr_to_pr[firstvr]
                        if first_pr == "invalid":
                            if firstvr in vr_to_spill:
                                first_pr, pr_nu, vr_to_pr, pr_to_vr, vr_to_spill, pr_stack = self.restore(firstvr,
                                                                                                          pr_nu,
                                                                                                          vr_to_pr,
                                                                                                          pr_to_vr,
                                                                                                          vr_to_spill,
                                                                                                          pr_stack,
                                                                                                          reserved_pr, marks, vr_to_val)
                            elif pr_stack:
                                first_pr = pr_stack.pop()
                            else:
                                first_pr, pr_nu, vr_to_pr, pr_to_vr, vr_to_spill = self.spill(firstvr, pr_nu, vr_to_pr,
                                                                                              pr_to_vr, vr_to_spill,
                                                                                              reserved_pr, marks, vr_to_val)
                            vr_to_pr[firstvr] = first_pr
                            pr_to_vr[first_pr] = firstvr
                            pr_nu[first_pr] = first_nu
                            firstop[2] = "r" + str(first_pr)
                        else:
                            pr_nu[first_pr] = first_nu
                            firstop[2] = "r" + str(first_pr)
                        marks.append(first_pr)
                    #print (pr_nu)
                    cur.first_operand = firstop
                    # Secondly to deal with the use case and second op
                    second_nu = secondop[3]
                    if second_nu != "empty":
                        if second_nu != "inf":
                            second_nu = int(second_nu)
                        else:
                            second_nu = float("inf")
                    else:
                        second_nu = float("inf")
                    if secondop[0] != "empty":
                        if secondop[1][0] == "r":
                            secondvr = int(secondop[1][1:])
                            second_pr = vr_to_pr[secondvr]
                            if second_pr == "invalid":
                                if secondvr in vr_to_spill:
                                    second_pr, pr_nu, vr_to_pr, pr_to_vr, vr_to_spill, pr_stack = self.restore(secondvr,
                                                                                                              pr_nu,
                                                                                                              vr_to_pr,
                                                                                                              pr_to_vr,
                                                                                                              vr_to_spill,
                                                                                                              pr_stack,
                                                                                                              reserved_pr, marks, vr_to_val)
                                elif pr_stack:
                                    second_pr = pr_stack.pop()
                                else:
                                    second_pr, pr_nu, vr_to_pr, pr_to_vr, vr_to_spill = self.spill(secondvr, pr_nu,
                                                                                                  vr_to_pr,
                                                                                                  pr_to_vr, vr_to_spill,
                                                                                                  reserved_pr, marks, vr_to_val)
                                vr_to_pr[secondvr] = second_pr
                                pr_to_vr[second_pr] = secondvr
                                pr_nu[second_pr] = second_nu
                                secondop[2] = "r" + str(second_pr)
                            else:
                                pr_nu[second_pr] = second_nu
                                secondop[2] = "r" + str(second_pr)
                            marks.append(second_pr)
                    cur.second_operand = secondop
                    if second_nu == float("inf") and secondop[2] != "empty":
                        vr_to_pr[pr_to_vr[second_pr]] = "invalid"
                        pr_to_vr[second_pr] = "invalid"
                        pr_nu[second_pr] = float("inf")
                        pr_stack.append(second_pr)
                    if first_nu == float("inf") and firstop[2] != "empty":
                        vr_to_pr[pr_to_vr[first_pr]] = "invalid"
                        pr_to_vr[first_pr] = "invalid"
                        pr_nu[first_pr] = float("inf")
                        pr_stack.append(first_pr)
                    # Now to handle the define cases
                    if thirdop[1][0] == "r":
                        third_nu = thirdop[3]
                        if third_nu != "empty":
                            if third_nu != "inf":
                                third_nu = int(third_nu)
                            else:
                                third_nu = float("inf")
                        else:
                            third_nu = float("inf")
                        thirdvr = int(thirdop[1][1:])
                        third_pr = vr_to_pr[thirdvr]
                        if third_pr == "invalid":
                            if thirdvr in vr_to_spill:
                                third_pr, pr_nu, vr_to_pr, pr_to_vr, vr_to_spill, pr_stack = self.restore(thirdvr,
                                                                                                          pr_nu,
                                                                                                          vr_to_pr,
                                                                                                          pr_to_vr,
                                                                                                          vr_to_spill,
                                                                                                          pr_stack,
                                                                                                          reserved_pr, marks, vr_to_val)
                            elif pr_stack:
                                third_pr = pr_stack.pop()
                            else:
                                third_pr, pr_nu, vr_to_pr, pr_to_vr, vr_to_spill = self.spill(thirdvr, pr_nu, vr_to_pr,
                                                                                              pr_to_vr, vr_to_spill,
                                                                                              reserved_pr, marks, vr_to_val)
                            vr_to_pr[thirdvr] = third_pr
                            pr_to_vr[third_pr] = thirdvr
                            pr_nu[third_pr] = third_nu
                            thirdop[2] = "r" + str(third_pr)
                        else:
                            pr_nu[third_pr] = third_nu
                            thirdop[2] = "r" + str(third_pr)
                        marks.append(third_pr)
                    cur.third_operand = thirdop
                    res = ""
                    res += reversed_dict[cur.get_opcode()]
                    res += " "
                    if cur.get_firstOperand()[2] != "empty":
                        res += cur.get_firstOperand()[2]
                    else:
                        if cur.get_firstOperand()[0] != "empty":
                            res += cur.get_firstOperand()[0]
                    if cur.get_secondOperand()[0] != "empty":
                        res += ", "
                        res += cur.get_secondOperand()[2]
                    if cur.get_thirdOperand()[0] != "empty":
                        res += " => "
                        res += cur.get_thirdOperand()[2]
                    print(res)
                    if cur.get_opcode() == 2:
                        vr_to_val[int(thirdop[1][1:])] = int(firstop[0])
                    cur = cur.next
        return self

    def spill(self, vr, pr_nu, vr_to_pr, pr_to_vr, vr_to_spill, reserved_pr, marks, vr_to_val):
        # first track the pr with farthest next use
        spilled_pr = None
        farthest = -float("inf")
        for i in range(0, len(pr_nu)):
            if pr_nu[i] != float("inf"):
                if pr_nu[i] > farthest and i not in marks:
                    farthest = pr_nu[i]
                    spilled_pr = i
        # delete all information regarding the old pr
        if not spilled_pr:
            spilled_pr = 0
        spilled_vr = pr_to_vr[spilled_pr]
        #print(spilled_vr, farthest, spilled_pr)
        pr_to_vr[spilled_pr] = "invalid"
        pr_nu[spilled_pr] = float("inf")
        vr_to_pr[spilled_vr] = "invalid"
        #now discuss whether the spilled vr is a loadI or not
        if vr_to_val[spilled_vr]:
            vr_to_spill[spilled_vr] = -vr_to_val[spilled_vr]
            return spilled_pr, pr_nu, vr_to_pr, pr_to_vr, vr_to_spill
        # add to vr to spill
        vr_to_spill[spilled_vr] = self.location_code
        self.location_code += 4
        # print the spill message
        print ("loadI " + str(self.location_code - 4) + " => r" + str(reserved_pr))
        print("store r" + str(spilled_pr) + " => r" + str(reserved_pr))
        return spilled_pr, pr_nu, vr_to_pr, pr_to_vr, vr_to_spill


    def restore(self, vr, pr_nu, vr_to_pr, pr_to_vr, vr_to_spill, pr_stack, reserved_pr, marks, vr_to_val):
        location = vr_to_spill[vr]
        if location < 0:
            del vr_to_spill[vr]
            if pr_stack:
                restored_pr = pr_stack.pop()
            else:
                restored_pr, pr_nu, vr_to_pr, pr_to_vr, vr_to_spill = self.spill(vr, pr_nu, vr_to_pr, pr_to_vr,
                                                                                 vr_to_spill, reserved_pr, marks, vr_to_val)
            print("loadI " + str(-location) + " => r" + str(restored_pr))
            return restored_pr, pr_nu, vr_to_pr, pr_to_vr, vr_to_spill, pr_stack
        # delete the key in vr_to_spill
        del vr_to_spill[vr]
        if pr_stack:
            restored_pr = pr_stack.pop()
        else:
            restored_pr, pr_nu, vr_to_pr, pr_to_vr, vr_to_spill = self.spill(vr, pr_nu, vr_to_pr, pr_to_vr, vr_to_spill, reserved_pr, marks, vr_to_val)
        # print the restore code
        print ("loadI " + str(location) + " => r" + str(reserved_pr))
        print ("load r" + str(reserved_pr) + " => r" + str(restored_pr))
        return restored_pr, pr_nu, vr_to_pr, pr_to_vr, vr_to_spill, pr_stack
































