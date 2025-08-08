from abc import ABC, abstractmethod

from app.schemas.customer import PutCustomerRequest


class CustomerInterface(ABC):

    @abstractmethod
    def save_customer_profile(self, customer_data: PutCustomerRequest):
        raise NotImplementedError()
