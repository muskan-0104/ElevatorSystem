# elevators/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Elevator
from .serializers import ElevatorSerializer
from rest_framework.decorators import action

def isElevatorWorking(elevator):
        return elevator.is_operational

class ElevatorViewSet(viewsets.ModelViewSet):
    queryset = Elevator.objects.all()
    req_list = {}
    max_elevators=5
    max_floors=15
    serializer_class = ElevatorSerializer

    @action(detail=False, methods=['post'])
    def initialize(self, request):
        num_elevators = request.data.get('num_elevators', self.max_elevators)
        for i in range(num_elevators):
            Elevator.objects.create()
        return Response({'message': f'{num_elevators} elevators initialized successfully'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def requests(self, request, pk=None):
        elevator = self.get_object()

        if pk in self.req_list:
            requests = self.req_list[pk]
            return Response({'message': f'Requests for elevator {requests} fetched successfully'})
        else:
            return Response({'message': f'No requests for elevator {pk} found'})

    @action(detail=True, methods=['get'])
    def next_destination(self, request, pk=None):
        elevator = self.get_object()

        if isElevatorWorking(elevator)==False:
            return Response({'message': f'Door of elevator {pk} is under maintenance.Opening Denied!'}, status=status.HTTP_401_UNAUTHORIZED)
        

        if pk in self.req_list and self.req_list[pk] != ():
        # Logic to fetch next destination for the given elevator
            next_destination_up = self.max_floors+1
            next_destination_down = -1
            next_destination=-1
            direction='UP'

            for i in self.req_list[pk]:
                floor = int(i)
                if floor-elevator.current_floor>0 and next_destination_up>floor:
                    next_destination_up=floor
                if elevator.current_floor-floor>0 and next_destination_down<floor:
                    next_destination_down = floor

            if elevator.direction=='UP' and next_destination_up!=self.max_floors+1:
                direction='UP'
                next_destination = next_destination_up
            elif elevator.direction=='UP' and next_destination_up==self.max_floors+1:
                direction='DOWN'
                next_destination=next_destination_down
            elif elevator.direction=='DOWN' and next_destination_down!=-1:
                direction='DOWN'
                next_destination = next_destination_down
            else:
                direction='UP'
                next_destination=next_destination_up

            if pk in self.req_list and next_destination!=-1 and next_destination!=self.max_floors+1:
                self.req_list[pk].remove(str(next_destination))
            else:
                 return Response({'message': f'No request provided'})
            elevator.current_floor=next_destination
            elevator.direction=direction
            elevator.save()

            serializer = ElevatorSerializer(elevator)

            return Response({
                'message': f'Next destination of {pk} is {elevator.current_floor} in {elevator.direction}!',
                'elevator_data': serializer.data,
            })
        return Response({'message': f'No request provided'})


    @action(detail=True, methods=['get'])
    def direction(self, request, pk=None):
        elevator = self.get_object()
        return Response({'message': f'Direction for elevator {pk} is {elevator.direction}!'})
    
    @action(detail=True, methods=['get'])
    def current_floor(self, request, pk=None):
        elevator = self.get_object()

        serializer = ElevatorSerializer(elevator)

        return Response({
            'message': f'Current Floor for elevator {pk} is {elevator.current_floor} in {elevator.direction}!',
            'elevator_data': serializer.data  # Include the serialized data in the response
        })
    
        # return Response({'message': f'Current Floor for elevator {pk} is {elevator.current_floor} in {elevator.direction}!'})

    @action(detail=True, methods=['post'], url_path='floor/(?P<floor>\d+)/save_request')
    def save_request(self, request, pk=None,floor=None):
        elevator = self.get_object()

        if isElevatorWorking(elevator)==False:
            return Response({'message': f'Door of elevator {pk} is under maintenance.Opening Denied!'}, status=status.HTTP_401_UNAUTHORIZED)
        

        if elevator.current_floor==int(floor):
            return Response({'message': f'We are already on {floor} floor'})

        if pk in self.req_list:
            self.req_list[pk].add(floor)
        else:
            self.req_list[pk]=set([floor])

        return Response({'message': f'Request saved for elevator {self.req_list[pk]}'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put'])
    def maintenance(self, request, pk=None):
        elevator = self.get_object()
        elevator.is_operational = False
        elevator.save()
        return Response({'message': f'Elevator {pk} marked as not working'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['put'])
    def maintenance_complete(self, request, pk=None):
        elevator = self.get_object()
        elevator.is_operational = True
        elevator.save()
        return Response({'message': f'Elevator {pk} marked as working'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def open_door(self, request, pk=None):
        elevator = self.get_object()
        if isElevatorWorking(elevator)==False:
            return Response({'message': f'Door of elevator {pk} is under maintenance.Opening Denied!'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({'message': f'Door of elevator {pk} opened successfully'})

    @action(detail=True, methods=['post'])
    def close_door(self, request, pk=None):
        elevator = self.get_object()
        if isElevatorWorking(elevator)==False:
            return Response({'message': f'Door of elevator {pk} is under maintenance.Closing Door is Denied!'}, status=status.HTTP_401_UNAUTHORIZED)
       
        return Response({'message': f'Door of elevator {pk} closed successfully'})
