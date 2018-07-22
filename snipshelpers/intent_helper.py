def getAllBySlotName(slots, slotName):
    return [slot for slot in slots if slotName == slot['slotName']]


def getFirstBySlotName(slots, slotName):
    filtered = getAllBySlotName(slots, slotName)
    if len(filtered) > 0:
        return filtered[0]
    else:
        return None
