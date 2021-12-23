class Helper:
    @staticmethod
    def get_element_from_list_by_id(element_id, list_):
        list_.sort(key=lambda x: x.id)
        index = int(str(element_id)[1:])-1
        try:
            return list_[index]
        except IndexError:
            print(str(index) + "----------------------------------")
