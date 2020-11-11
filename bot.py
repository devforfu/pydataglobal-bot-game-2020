"""Supply Chain Game entry point.

The game consists of four agents interacting with each other as the diagram shows:

                     orders                orders                   orders                 orders
demand             --------->             --------->              --------->              --------->
------> (RETAILER)            (WHOLESALER)           (DISTRIBUTOR)          (MANUFACTURER)
                   <---------             <---------              <---------              <---------
                    shipments             shipments                shipments               shipments

The agents form a supply chain, i.e. each agent can send a request to its neighbour and ask for a delivery of a
certain amount of goods. The neighbour does a shipment but also orders delivery from the next entity in the chain
in case of getting out of stock. The game unrolls in a turn-based fashion: all agents take decisions about the number
of items to order simultaneously, then a next turn starts.

A retailer is the first agent in the chain. It gets demand from customers and should keep them fulfilled ordering more
items from agents next in the chain.

A manufacturer is the last agent in the chain. It "orders" items from an infinite supply and ships them down the chain.

The problem is that the agents don't know the current numbers of the stock level of their partners. Also, the
order/shipment exchange doesn't happen instantaneously but involves two turns of delay. (Except manufacturer that
refills its supply with a delay of one turn). Therefore, non-optimal orderings could lead to stock-outs or too many
items hold. Both conditions lead to costs.

Your goal is to implement a strategy for each of the four agents in such a way, that the costs are minimal after
20 game turns. It means that you should try to escape both shortages AND holding too many items in stock. Your strategy
shouldn't use any other information except stored in a dictionary that is given to `get_action()` method. Also, the
agents are not allowed to communicate their stock levels or any other internal information to each other.

In this file, you'll find a dummy implementation for each agent that orders a random amount of items each turn. If you
run this script as-is, you'll see that the costs at the end of the game are very high. Try to come up with a better
solution!
"""
import numpy as np

from supply_chain_env.envs.env import SupplyChainBotTournament
from supply_chain_env.leaderboard import post_score_to_api


class Retailer:

    def get_action(self, step_state: dict) -> int:
        return np.random.randint(0, 4)


class Wholesaler:

    def get_action(self, step_state: dict) -> int:
        return np.random.randint(0, 4)


class Distributor:

    def get_action(self, step_state: dict) -> int:
        return np.random.randint(0, 4)


class Manufacturer:

    def get_action(self, step_state: dict) -> int:
        return np.random.randint(0, 4)


def main():
    env = SupplyChainBotTournament(
        env_type="classical"
    )  # TODO: decide if we should support all 3 environments or support one

    agents = [Retailer(), Wholesaler(), Distributor(), Manufacturer()]
    step_state = env.reset()
    while not env.done:
        env.render()
        actions = [a.get_action(step_state[i]) for i, a in enumerate(agents)]
        step_state, step_rewards, done, _ = env.step(actions)

    # get total costs and post results to leaderboard api
    total_costs = 0
    for step in step_state:
        total_costs += step["cum_cost"]
    post_score_to_api(score=total_costs)


if __name__ == "__main__":
    main()

