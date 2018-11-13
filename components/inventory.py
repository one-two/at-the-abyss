import libtcodpy as libtcod

from game_messages import Message

class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []
    
    def add_item(self, item):
        results = []

        if len(self.items) >= self.capacity:
            results.append({
                'item_added' : None,
                'message': Message('A mala ta cheia', libtcod.yellow)
                })
        else:
            results.append({
                'item_added': item,
                'message': Message('voce pegou {0}'.format(item.name), libtcod.blue)
            })
            self.items.append(item)
        return results

    def use_item(self, item):
        results = []
        results.append({
            'item_added' : None,
            'message': Message('Usou {0}'.format(item.name), libtcod.yellow)
            })
    
    def use(self, item_entity, **kwargs):
        results = []

        item_component = item_entity.item

        if item_component.use_function is None:
            results.append({'message': Message('{0} nao e usavel'.format(item_entity.name), libtcod.yellow)})
        else:
            kwargs = {**item_component.function_kwargs, **kwargs}
            item_use_results = item_component.use_function(self.owner, **kwargs)

            for item_use_result in item_use_results:
                if item_use_result.get('consumed'):
                    self.remove_item(item_entity)

            results.extend(item_use_results)

        return results

    def remove_item(self, item):
        self.items.remove(item)