from typing import *
import inspect
import sys
import itertools

class Router:
    _routes: Dict[str, Callable] = {}

    @classmethod
    def add(cls, obj: Union[Callable, type]) -> Union[Callable, type]:
        if inspect.isclass(obj):
            #cls.add(obj.__init__)
            return cls.wrap_class(obj)
        else:
            arg_types = [arg for arg in list(inspect.signature(obj).parameters.values()) if arg.name != "self"]
            arg_type = arg_types[0].annotation
            return_type = inspect.signature(obj).return_annotation
            if not isinstance(arg_type, str):
                arg_type = arg_type.__name__
            if not isinstance(return_type, str):
                return_type = return_type.__name__
            cls._routes[f"{arg_type} -> {return_type}"] = obj
            return obj

    @classmethod
    def wrap_class(cls, newcls: type) -> type:
        '''Here, we add a method __rshift__ that allows a >> to be used as a form of type coercion, defined by pre-registered routes in _routes.
        '''
        def __rshift__(self, target_type: type) -> type:
            # First, we check if there is a key in _routes with the newcls -> target_type.
            print(cls._routes)
            if not isinstance(target_type, str):
                target_type_name = target_type.__name__
            else:
                target_type_name = target_type
            if f"{newcls.__name__} -> {target_type_name}" in cls._routes:
                converter_func = cls._routes[f"{newcls.__name__} -> {target_type_name}"]
                converted_obj = converter_func(self)
                return converted_obj
            else:
                for i in range(6):
                    print(i)
                    try:
                        return cls.check_for_shortcuts(newcls.__name__, target_type_name, self)
                    except TypeError as e:
                        print(e)
                        continue
                else:
                    raise RuntimeError(f"No conversion from {newcls.__name__} to {target_type_name}")
        # And it's not strictly necessary, but if the class doesn't have a __repr__, we can make one:
        def __repr__(self):
            return f"{newcls.__name__}({self.__dict__})"
        try:
            newcls.__repr__ = __repr__
            newcls.__rshift__ = __rshift__
        except TypeError:
            # This usually means we're trying to add a method to a built-in type. So we just need to do this:
            class newcls2(newcls):
                pass
            newcls2.__rshift__ = __rshift__
            newcls2.__repr__ = __repr__
            newcls2.__name__ = newcls.__name__
            return newcls2
        return newcls

    @classmethod
    def split_arrow(cls, string: str) -> Tuple[str, str]:
        origin_type, end_type = string.split("->")
        origin_type = origin_type.strip()
        end_type = end_type.strip()
        return origin_type, end_type

    @classmethod
    def check_for_shortcuts(cls, origin_type: str, target_type: str, object_to_be_converted: Any = None) -> Any:
        '''
        If we wanted to call String("yellow") >> Review, without this function, we would get an error.
        Say we have two existing routes. A -> B, and B -> C.
        We want to convert A to C.
        Therefore, we get routes_starting_with_origin_type: all routes that start with A, and routes_ending_with_target_type: all routes ending with C.
        That might look like this:
        routes_starting_with_origin_type: [(A, B)]
        routes_ending_with_target_type: [(B, C)]
        Is B the same in both routes? Yes! That's good because we can create a new route of A -> C, and create a function that calls A->B, then B->C.
        '''
        routes_starting_with_origin_type: List[Tuple[str, str]] = [cls.split_arrow(key) for key in cls._routes.keys() if key.startswith(f"{origin_type} ->")]
        routes_ending_with_target_type: List[Tuple[str, str]] = [cls.split_arrow(key) for key in cls._routes.keys() if key.endswith(f"-> {target_type}")]
        print(f"routes_starting_with_origin_type: {routes_starting_with_origin_type}")
        print(f"routes_ending_with_target_type: {routes_ending_with_target_type}")
        matching_route_pairs: List[Tuple[Tuple, Tuple]] = []
        for route_pair in routes_starting_with_origin_type:
            for route_pair2 in routes_ending_with_target_type:
                if route_pair[1] == route_pair2[0]:
                    matching_route_pairs.append((route_pair, route_pair2))
        if len(matching_route_pairs) == 0:
            # Just in case there's a third level of indirection:
            all_routes: List[Tuple[str, str]] = [cls.split_arrow(key) for key in cls._routes.keys()]
            for route1 in all_routes:
                for route2 in all_routes:
                    if route1[1] == route2[0]:
                        matching_route_pairs.append((route1, route2))
        # At this point, we have at least one matching route. So now we turn the tuples back into arrows, get their associated functions, and create a new function that calls the first, gets the result, then calls the second with the result.
        for pair in matching_route_pairs:
            func1 = cls._routes[f"{pair[0][0]} -> {pair[0][1]}"]
            func2 = cls._routes[f"{pair[1][0]} -> {pair[1][1]}"]
            if pair[0][0] == pair[1][1]:
                # This means we're looking at A -> A which is pretty useless
                continue
            print(f"func1: {func1.__name__}")
            print(f"func2: {func2.__name__}")
            def combined_func(obj: Any) -> Any:
                obj = func1(obj)
                return func2(obj)
            new_arrow_route = f"{pair[0][0]} -> {pair[1][1]}"
            print(new_arrow_route)
            if new_arrow_route in cls._routes:
                return cls._routes[new_arrow_route](object_to_be_converted)
            cls._routes[new_arrow_route] = combined_func
            if new_arrow_route == f"{origin_type} -> {target_type}":
                print("Found one! Returning it.")
                print(cls._routes)
                return combined_func(object_to_be_converted)
        else:
            raise TypeError("No conversion from {} to {}".format(origin_type, target_type))


coerce = Router.add       
