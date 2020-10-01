from fitbit.api import Fitbit


class CustomFitbit(Fitbit):
    def activity_summary(self, user_id: str, date: str):
        url = "{0}/{1}/user/{2}/activities/date/{3}.json".format(
            *self._get_common_args(user_id), date)
        return self.make_request(url)

    def food_summary(self, user_id: str, date: str):
        url = "{0}/{1}/user/{2}/foods/log/date/{3}.json".format(
            *self._get_common_args(user_id), date)
        return self.make_request(url)

    def water_summary(self, user_id: str, date: str):
        url = "{0}/{1}/user/{2}/foods/log/water/date/{3}.json".format(
            *self._get_common_args(user_id), date)
        return self.make_request(url)
