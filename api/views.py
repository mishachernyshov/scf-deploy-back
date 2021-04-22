from django.shortcuts import render
from .permissions import IsAuthorOrReadOnly, IsCartUserOrReadOnly
from rest_framework.permissions import AllowAny
from rest_framework import generics, permissions
from api.models import Component, ComponentReport, WebStore, \
    WebStoreComponent, AssembledConstruction, ConstructionComponent, \
    ConstructionReport, Cart
from api.serializers import ComponentSerializer, ComponentReportSerializer, \
    WebStoreSerializer, WebStoreComponentSerializer, \
    AssembledConstructionSerializer, ConstructionComponentSerializer, \
    ConstructionReportSerializer, UserSerializer, CartSerializer, \
    AppropriateConstructionSerializer
from django.contrib.auth import get_user_model
import psycopg2
from psycopg2 import Error
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import filters
import serial
import smtplib

User = get_user_model()


class ComponentList(generics.ListCreateAPIView):
    """
    The list which contains all the components set out in the system.
    The API provided by this VIEW can be used to view and create objects.
    """
    permission_classes = (AllowAny,)
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer


class ComponentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Information about certain components.
    The API provided by this VIEW can be used to view, edit or delete the object.
    """
    permission_classes = (AllowAny,)
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer


class ComponentReportList(generics.ListCreateAPIView):
    """
    The list which contains all reports about all components which are
    available in the system.
    The API provided by this VIEW can be used to view and create objects.
    """
    permission_classes = (AllowAny,)
    queryset = ComponentReport.objects.all()
    serializer_class = ComponentReportSerializer


class ComponentReportDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Information about a certain component report.
    The API provided by this VIEW can be used to view, edit or delete the object.
    """
    permission_classes = (AllowAny,)
    queryset = ComponentReport.objects.all()
    serializer_class = ComponentReportSerializer


class WebStoreList(generics.ListCreateAPIView):
    """
    The list which contains all webstores that provide info about components they sell.
    The API provided by this VIEW can be used to view and create objects.
    """
    queryset = WebStore.objects.all()
    serializer_class = WebStoreSerializer


class WebStoreDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Information about a certain webstore.
    The API provided by this VIEW can be used to view, edit or delete the object.
    """
    queryset = WebStore.objects.all()
    serializer_class = WebStoreSerializer


class WebStoreComponentList(generics.ListCreateAPIView):
    """
    The list which contains pairs of a webstore and info about component it sells.
    The API provided by this VIEW can be used to view and create objects.
    """
    queryset = WebStoreComponent.objects.all()
    serializer_class = WebStoreComponentSerializer


class WebStoreComponentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Information about a single pair of a webstore and info about component it sells.
    The API provided by this VIEW can be used to view, edit or delete the object.
    """
    queryset = WebStoreComponent.objects.all()
    serializer_class = WebStoreComponentSerializer


class AssembledConstructionList(generics.ListCreateAPIView):
    """
    The list which contains pairs of a webstore and info about component it sells.
    The API provided by this VIEW can be used to view and create objects.
    """
    permission_classes = (AllowAny,)
    queryset = AssembledConstruction.objects.all()
    serializer_class = AssembledConstructionSerializer


class AssembledConstructionDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Information about a single pair of a webstore and info about component it sells.
    The API provided by this VIEW can be used to view, edit or delete the object.
    """
    permission_classes = (AllowAny,)
    queryset = AssembledConstruction.objects.all()
    serializer_class = AssembledConstructionSerializer


class ConstructionComponentList(generics.ListCreateAPIView):
    """
    The list which contains pairs of a webstore and info about component it sells.
    The API provided by this VIEW can be used to view and create objects.
    """
    queryset = ConstructionComponent.objects.all()
    serializer_class = ConstructionComponentSerializer


class ConstructionComponentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Information about a single pair of a webstore and info about component it sells.
    The API provided by this VIEW can be used to view, edit or delete the object.
    """
    queryset = ConstructionComponent.objects.all()
    serializer_class = ConstructionComponentSerializer


class ConstructionReportList(generics.ListCreateAPIView):
    """
    The list which contains pairs of a webstore and info about component it sells.
    The API provided by this VIEW can be used to view and create objects.
    """
    permission_classes = (AllowAny,)
    queryset = ConstructionReport.objects.all()
    serializer_class = ConstructionReportSerializer


class ConstructionReportDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Information about a single pair of a webstore and info about component it sells.
    The API provided by this VIEW can be used to view, edit or delete the object.
    """
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = ConstructionReport.objects.all()
    serializer_class = ConstructionReportSerializer


class UserList(generics.ListCreateAPIView):
    """
    The list which contains pairs of a webstore and info about component it sells.
    The API provided by this VIEW can be used to view and create objects.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Information about a single pair of a webstore and info about component it sells.
    The API provided by this VIEW can be used to view, edit or delete the object.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CartList(generics.ListCreateAPIView):
    """
    The list which contains pairs of a webstore and info about component it sells.
    The API provided by this VIEW can be used to view and create objects.
    """
    permission_classes = (IsCartUserOrReadOnly,)
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Information about a single pair of a webstore and info about component it sells.
    The API provided by this VIEW can be used to view, edit or delete the object.
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


def general_construction_selection(query_params, mode):
    params_dict = query_params
    components = list(map(int, list(params_dict.getlist('0'))))
    constructions_id = [k.id for k in
                        AssembledConstruction.objects.all()]

    appropriate_constructions = []

    for k in constructions_id:
        fail_count = 0
        constr_components = [n.component.id for n in
                             ConstructionComponent.objects.filter(construction_id=k)]
        component_copy = components.copy()
        for i in constr_components:
            try:
                component_index = component_copy.index(i)
            except ValueError:
                component_index = -1
            if component_index != -1:
                component_copy.pop(component_index)
            else:
                fail_count += 1
                if fail_count > 2 or mode == 'precise':
                    break
        if (mode == 'precise' and not fail_count) or \
                (mode == 'imprecise' and (fail_count == 1 or fail_count == 2)):
            appropriate_constructions.append(k)
        continue
    appropriate_constructions_query_set = \
        AssembledConstruction.objects.filter(id__in=appropriate_constructions)
    return appropriate_constructions_query_set


class AppropriateConstructionsForGivenComponents(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AppropriateConstructionSerializer

    def get_queryset(self):
        print(self.request.query_params)
        appropriate_constructions = \
            general_construction_selection(self.request.query_params, 'precise')

        return appropriate_constructions


class AlmostAppropriateConstructionsForGivenComponents(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AppropriateConstructionSerializer

    def get_queryset(self):
        appropriate_constructions = \
            general_construction_selection(self.request.query_params, 'imprecise')

        return appropriate_constructions


def connect_to_database():
    return psycopg2.connect(user="postgres",
                            password="Xpohuc490",
                            host="127.0.0.1",
                            port="5432",
                            database="sfc-db")


def disconnect_from_database(connection, cursor):
    if connection:
        cursor.close()
        connection.close()


def executeRequest(request_string, query_proc_func, container, request_type):
    ps_connection = None
    cursor = None

    try:
        ps_connection = connect_to_database()

        cursor = ps_connection.cursor()
        cursor.execute(request_string)
        if request_type == 'GET':
            fetch_data = cursor.fetchall()
            query_proc_func(fetch_data, container)
        else:
            ps_connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        disconnect_from_database(ps_connection, cursor)
    if request_type == 'GET':
        print(container)
        return Response(container)


def getCartGoods(requested_data, container):
    for row in requested_data:
        container[row[0]] = [row[1], row[2]]


def getComponentWebShops(requested_data, container):
    for row in requested_data:
        container[row[0]] = [row[1], row[2], row[3], row[4]]


def getConstructionComponents(requested_data, container):
    for row in requested_data:
        container[row[1]] = [row[2], row[0]]


def getReports(requested_data, container):
    for row in requested_data:
        container['reports'].append([row[0], row[1], row[2]])


def getComponentsByType(requested_data, container):
    if len(requested_data):
        for row in requested_data:
            if row[0] not in container.keys():
                container[row[0]] = []
            container[row[0]].append([row[1],
                                      'http://127.0.0.1:8000/images/' + row[2]])


def getConstructionInstructionData(requested_data, container):
    if len(requested_data):
        construction_name = requested_data[0][0]
        construction_instruction = requested_data[0][1]
        construction_images = requested_data[0][2]
        all_actions = []
        with open("static/images/" + construction_instruction, "r", encoding="utf-8") as file:
            line = file.readline().rstrip('\n')
            all_actions.append(line)
            while line := file.readline().rstrip('\n'):
                action_to_do = [line]
                line = file.readline().rstrip('\n')
                action_to_do.append(line)
                all_actions.append(action_to_do)
        image_set = []
        with open("static/images/" + construction_images, "r", encoding="utf-8") as file:
            for line in file:
                image_set.append(line.rstrip('\n'))
        container['name'] = construction_name
        container['instruction'] = all_actions
        container['images'] = image_set


class CartContentGetting(generics.ListAPIView):
    permission_classes = (AllowAny,)

    cart_stastistics_request = "SELECT api_assembledconstruction.name, " \
                               "COUNT(api_assembledconstruction.name), api_assembledconstruction.id FROM api_cart" \
                               " INNER JOIN api_assembledconstruction ON " \
                               "api_cart.construction_id = api_assembledconstruction.id " \
                               "WHERE api_cart.user_id = {0} AND " \
                               "api_cart.construction_id = api_assembledconstruction.id " \
                               "GROUP BY api_assembledconstruction.name, api_assembledconstruction.id"

    delete_cart_items = "DELETE FROM api_cart WHERE api_cart.id IN " \
                        "(SELECT api_cart.id FROM api_cart " \
                        "WHERE api_cart.construction_id = {0} " \
                        "AND api_cart.user_id = {1} LIMIT {2})"

    add_cart_items = "DO $$ DECLARE counter integer := 0; BEGIN " \
                     "WHILE counter < {0} loop INSERT INTO " \
                     "api_cart(user_id, construction_id) VALUES({1}, {2}); " \
                     "counter := counter + 1; END LOOP; END$$;"

    delete_redundant_items = "DELETE FROM api_cart WHERE api_cart.id IN " \
                             "(SELECT api_cart.id FROM api_cart " \
                             "WHERE api_cart.construction_id NOT IN ({0}) " \
                             "AND api_cart.user_id = {1})"

    def get(self, request):
        user_cart_data = {}
        return executeRequest(
            CartContentGetting.cart_stastistics_request.format(request.user.id),
            getCartGoods, user_cart_data, 'GET')

    def post(self, request):
        user_construction_values = []
        print(request.data)
        for k in request.data['new_values']:
            print(k)
            requested_construction = k['construction_id']
            initial_count = k['initial_count']
            requested_count = k['requested_count']
            if requested_count < initial_count:
                executeRequest(CartContentGetting.delete_cart_items.format(
                    requested_construction, request.user.id,
                    initial_count - requested_count), None, None, 'DELETE')
            elif requested_count > initial_count:
                executeRequest(CartContentGetting.add_cart_items.format(
                    requested_count - initial_count, request.user.id,
                    requested_construction), None, None, 'POST')
            user_construction_values.append(requested_construction)
        executeRequest(CartContentGetting.delete_redundant_items.format(
            str(user_construction_values)[1:-1], request.user.id),
            None, None, 'DELETE')
        return Response({})


class EmptyUserCart(generics.ListAPIView):
    permission_classes = (AllowAny,)

    request = "DELETE FROM api_cart WHERE api_cart.user_id = {0}"

    def post(self, request):
        executeRequest(EmptyUserCart.request.format(
            request.user.id), None, None, 'DELETE')
        return Response({})


class UserConstructionList(generics.ListAPIView):
    permission_classes = (AllowAny,)

    construction_list_request = "SELECT api_assembledconstruction.name, " \
                                "api_assembledconstruction.image, api_assembledconstruction.id " \
                                "FROM api_userconstruction INNER JOIN api_assembledconstruction ON " \
                                "api_userconstruction.construction_id = api_assembledconstruction.id " \
                                "WHERE api_userconstruction.user_id = {0}"

    def get(self, request):
        user_constructions = {}
        return executeRequest(
            UserConstructionList.construction_list_request.format(request.user.id),
            getCartGoods, user_constructions, 'GET')


class BoughtAssembledConstructionList(generics.ListAPIView):
    permission_classes = (AllowAny,)

    user_constructions_statistics_request = "SELECT DISTINCT(api_assembledconstruction.name, " \
                                            "api_assembledconstruction.image, api_assembledconstruction.id) " \
                                            "FROM api_assembledconstruction INNER JOIN api_userconstruction " \
                                            "ON api_userconstruction.construction_id = " \
                                            "api_assembledconstruction.id WHERE api_userconstruction.user_id = {0}"

    def get(self, request):
        user_construction_data = {}
        return executeRequest(
            BoughtAssembledConstructionList.user_constructions_statistics_request.format(
                request.user.id), getCartGoods, user_construction_data, 'GET')


class ConstructionInstruction(generics.ListAPIView):
    permission_classes = (AllowAny,)

    construction_info_request = "SELECT api_assembledconstruction.name, " \
                                "api_assembledconstruction.assemble_instruction, " \
                                "api_assembledconstruction.instruction_images " \
                                "FROM api_assembledconstruction WHERE api_assembledconstruction.id = {0}"

    def get(self, request, *args, **kwargs):
        user_construction_data = {}
        return executeRequest(
            ConstructionInstruction.construction_info_request.format(kwargs['pk']),
            getConstructionInstructionData, user_construction_data, 'GET')


class WebShopsForComponent(generics.ListAPIView):
    permission_classes = (AllowAny,)

    web_shops_request = "SELECT api_webstore.name, api_webstore.logo, " \
                        "api_webstore.homepage, api_webstorecomponent.price, " \
                        "api_webstorecomponent.component_page_link " \
                        "FROM api_webstore INNER JOIN api_webstorecomponent " \
                        "ON api_webstore.id = api_webstorecomponent.web_store_id " \
                        "WHERE api_webstorecomponent.component_id = {0}"

    def get(self, request, *args, **kwargs):
        web_shops = {}
        return executeRequest(
            WebShopsForComponent.web_shops_request.format(kwargs['pk']),
            getComponentWebShops, web_shops, 'GET')


class ConstructionComponents(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)

    components_fetching_request = "SELECT api_component.id, api_component.name, " \
                                  "api_component.image " \
                                  "FROM api_component INNER JOIN api_constructioncomponent " \
                                  "ON api_component.id = api_constructioncomponent.component_id " \
                                  "WHERE api_constructioncomponent.construction_id = {0}"

    def get(self, request, *args, **kwargs):
        components = {}
        return executeRequest(
            ConstructionComponents.components_fetching_request.format(kwargs['pk']),
            getConstructionComponents, components, 'GET')


class ComponentConstructions(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)

    constructions_fetching_request = "SELECT api_assembledconstruction.id, " \
                                     "api_assembledconstruction.name, " \
                                     "api_assembledconstruction.image FROM api_assembledconstruction " \
                                     "INNER JOIN api_constructioncomponent ON api_assembledconstruction.id " \
                                     "= api_constructioncomponent.construction_id WHERE " \
                                     "api_constructioncomponent.component_id = {0}"

    def get(self, request, *args, **kwargs):
        constructions = {}
        return executeRequest(
            ComponentConstructions.constructions_fetching_request.format(kwargs['pk']),
            getConstructionComponents, constructions, 'GET')


class ComponentReports(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)

    component_report_request = "SELECT auth_user.username, " \
                               "api_componentreport.publication_date, api_componentreport.text FROM " \
                               "api_component INNER JOIN api_componentreport ON api_component.id = " \
                               "api_componentreport.component_id INNER JOIN auth_user ON " \
                               "api_componentreport.author_id = auth_user.id WHERE api_component.id = {0} " \
                               "ORDER BY api_componentreport.publication_date"

    def get(self, request, *args, **kwargs):
        reports = {'reports': []}
        return executeRequest(
            ComponentReports.component_report_request.format(kwargs['pk']),
            getReports, reports, 'GET')


class ConstructionReports(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)

    construction_report_request = "SELECT auth_user.username, " \
                                  "api_constructionreport.publication_date, api_constructionreport.text " \
                                  "FROM api_assembledconstruction INNER JOIN api_constructionreport ON " \
                                  "api_assembledconstruction.id = api_constructionreport.construction_id " \
                                  "INNER JOIN auth_user ON api_constructionreport.author_id = auth_user.id " \
                                  "WHERE api_assembledconstruction.id = {0} ORDER BY api_constructionreport.publication_date"

    def get(self, request, *args, **kwargs):
        reports = {'reports': []}
        return executeRequest(
            ConstructionReports.construction_report_request.format(kwargs['pk']),
            getReports, reports, 'GET')


class ComponentsByType(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)

    component_by_type_request = "SELECT api_component.type, api_component.name, " \
                                "api_component.image FROM api_component ORDER BY api_component.type"

    def get(self, request, *args, **kwargs):
        components = {}
        return executeRequest(
            ComponentsByType.component_by_type_request,
            getComponentsByType, components, 'GET')


class AdditionUserConstruction(generics.CreateAPIView):
    permission_classes = (AllowAny,)

    addition_request = "INSERT INTO api_cart(construction_id, " \
                       "user_id) VALUES({0}, {1})"

    def post(self, request):
        executeRequest(AdditionUserConstruction.addition_request.format(
            request.data['construction'], request.user.id), None, None, 'POST')
        return Response({})


class AdditionConstructionReport(generics.CreateAPIView):
    permission_classes = (AllowAny,)

    addition_request = "INSERT INTO api_constructionreport(author_id, " \
                       "construction_id, text, publication_date) " \
                       "VALUES({0}, {1}, '{2}', NOW())"

    def post(self, request):
        executeRequest(AdditionConstructionReport.addition_request.format(
            request.user.id, request.data['construction'], request.data['text']),
            None, None, 'POST')
        return Response({})


class AdditionComponentReport(generics.CreateAPIView):
    permission_classes = (AllowAny,)

    addition_request = "INSERT INTO api_componentreport(author_id, " \
                       "component_id, text, publication_date) " \
                       "VALUES({0}, {1}, '{2}', NOW())"

    def post(self, request):
        print(request.user.id)
        print(request.data['component'])
        print(request.data['text'])
        executeRequest(AdditionComponentReport.addition_request.format(
            request.user.id, request.data['component'], request.data['text']),
            None, None, 'POST')
        return Response({})


class TemperatureValue(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ConstructionComponentSerializer

    def get(self, request):
        s = serial.Serial('COM3')
        res = s.readline().decode('utf-8').rstrip()
        value = 0.
        try:
            value = float(res)
        except:
            ...
        print(res)
        return Response({'value': value})
