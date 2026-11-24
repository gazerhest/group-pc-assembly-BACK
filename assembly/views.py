from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Build, Category, Manufacturer, Part, Review


def error_response(message, status_code, details=None):
    data = {'error': message}
    if details:
        data['details'] = details
    return Response(data, status=status_code)


class CategoryList(APIView):
    # TODO: add permissions

    def get(self, request):
        categories = Category.objects.all().order_by('name')
        # TODO: add serialization
        return Response(
            list(categories.values('id', 'name', 'description')),
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        # TODO: add serialization
        if not request.data:
            return error_response(
                'Invalid data for category creation.',
                status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {'detail': 'TODO: add serialization'},
            status=status.HTTP_201_CREATED,
        )


class CategoryDetail(APIView):
    # TODO: add permissions

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None

    def get(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return error_response(f'Category with ID {pk} not found.', status.HTTP_404_NOT_FOUND)
        # TODO: add serialization
        return Response(
            {
                'id': category.id,
                'name': category.name,
                'description': category.description,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return error_response(f'Category with ID {pk} not found.', status.HTTP_404_NOT_FOUND)
        # TODO: add serialization
        if not request.data:
            return error_response(
                'Invalid data for category update.',
                status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {'detail': 'TODO: add serialization'},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return error_response(f'Category with ID {pk} not found.', status.HTTP_404_NOT_FOUND)

        parts_count = category.parts.count()
        if parts_count > 0:
            return error_response(
                f"Cannot delete category '{category.name}' because it has {parts_count} related part(s).",
                status.HTTP_409_CONFLICT,
            )
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ManufacturerList(APIView):
    # TODO: add permissions

    def get(self, request):
        manufacturers = Manufacturer.objects.all().order_by('name')
        # TODO: add serialization
        return Response(
            list(manufacturers.values('id', 'name', 'country', 'website', 'description')),
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        # TODO: add serialization
        if not request.data:
            return error_response(
                'Invalid data for manufacturer creation.',
                status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {'detail': 'TODO: add serialization'},
            status=status.HTTP_201_CREATED,
        )


class ManufacturerDetail(APIView):
    # TODO: add permissions

    def get_object(self, pk):
        try:
            return Manufacturer.objects.get(pk=pk)
        except Manufacturer.DoesNotExist:
            return None

    def get(self, request, pk):
        manufacturer = self.get_object(pk)
        if manufacturer is None:
            return error_response(f'Manufacturer with ID {pk} not found.', status.HTTP_404_NOT_FOUND)
        # TODO: add serialization
        return Response(
            {
                'id': manufacturer.id,
                'name': manufacturer.name,
                'country': manufacturer.country,
                'website': manufacturer.website,
                'description': manufacturer.description,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk):
        manufacturer = self.get_object(pk)
        if manufacturer is None:
            return error_response(f'Manufacturer with ID {pk} not found.', status.HTTP_404_NOT_FOUND)
        # TODO: add serialization
        if not request.data:
            return error_response(
                'Invalid data for manufacturer update.',
                status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {'detail': 'TODO: add serialization'},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):
        manufacturer = self.get_object(pk)
        if manufacturer is None:
            return error_response(f'Manufacturer with ID {pk} not found.', status.HTTP_404_NOT_FOUND)

        parts_count = manufacturer.parts.count()
        if parts_count > 0:
            return error_response(
                f"Cannot delete manufacturer '{manufacturer.name}' because it has {parts_count} related part(s).",
                status.HTTP_409_CONFLICT,
            )
        manufacturer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PartList(APIView):
    # TODO: add permissions

    def get(self, request):
        parts = Part.objects.all()

        category_id = request.query_params.get('category')
        manufacturer_id = request.query_params.get('manufacturer')
        search = request.query_params.get('search')

        try:
            if category_id:
                parts = parts.filter(category_id=category_id)
            if manufacturer_id:
                parts = parts.filter(manufacturer_id=manufacturer_id)
            if search:
                parts = parts.filter(title__icontains=search)
        except ValueError:
            return error_response('Not correct search query.', status.HTTP_400_BAD_REQUEST)

        # TODO: add filtering, sorting, pagination and serialization
        return Response(
            list(parts.values(
                'id', 'title', 'category_id', 'manufacturer_id', 'price', 'rating', 'specs', 'description', 'created_at'
            )),
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        # TODO: add serialization
        if not request.data:
            return error_response(
                'Invalid data for part creation.',
                status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {'detail': 'TODO: add serialization'},
            status=status.HTTP_201_CREATED,
        )


class PartDetail(APIView):
    # TODO: add permissions

    def get_object(self, pk):
        try:
            return Part.objects.get(pk=pk)
        except Part.DoesNotExist:
            return None

    def get(self, request, pk):
        part = self.get_object(pk)
        if part is None:
            return error_response(f'Part with ID {pk} not found.', status.HTTP_404_NOT_FOUND)
        # TODO: add serialization
        return Response(
            {
                'id': part.id,
                'title': part.title,
                'category': part.category.name,
                'manufacturer': part.manufacturer.name,
                'price': part.price,
                'rating': part.rating,
                'specs': part.specs,
                'description': part.description,
                'created_at': part.created_at,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk):
        part = self.get_object(pk)
        if part is None:
            return error_response(f'Part with ID {pk} not found.', status.HTTP_404_NOT_FOUND)
        # TODO: add serialization
        if not request.data:
            return error_response(
                'Invalid data for part update.',
                status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {'detail': 'TODO: add serialization'},
            status=status.HTTP_200_OK,
        )

    def patch(self, request, pk):
        part = self.get_object(pk)
        if part is None:
            return error_response(f'Part with ID {pk} not found.', status.HTTP_404_NOT_FOUND)
        # TODO: add serialization
        if not request.data:
            return error_response(
                'Invalid data for part update.',
                status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {'detail': 'TODO: add serialization'},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):
        part = self.get_object(pk)
        if part is None:
            return error_response(f'Part with ID {pk} not found.', status.HTTP_404_NOT_FOUND)
        part.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PartCompare(APIView):
    def get(self, request):
        ids_param = request.query_params.get('ids', '')
        if not ids_param:
            return error_response('Query parameter ids is required.', status.HTTP_400_BAD_REQUEST)

        try:
            part_ids = [int(item.strip()) for item in ids_param.split(',') if item.strip()]
        except ValueError:
            return error_response('Part IDs must be integers.', status.HTTP_400_BAD_REQUEST)

        parts = Part.objects.filter(id__in=part_ids)
        # TODO: check same category and add serialization
        return Response(
            list(parts.values('id', 'title', 'category__name', 'price', 'specs')),
            status=status.HTTP_200_OK,
        )


class PartReviewList(APIView):
    # TODO: add permissions

    def get(self, request, pk):
        try:
            part = Part.objects.get(pk=pk)
        except Part.DoesNotExist:
            return error_response(f'Part with ID {pk} not found.', status.HTTP_404_NOT_FOUND)

        reviews = part.reviews.all().order_by('-created_at')
        # TODO: add serialization
        return Response(
            list(reviews.values('id', 'author__username', 'rating', 'comment', 'created_at')),
            status=status.HTTP_200_OK,
        )

    def post(self, request, pk):
        try:
            part = Part.objects.get(pk=pk)
        except Part.DoesNotExist:
            return error_response(f'Part with ID {pk} not found.', status.HTTP_404_NOT_FOUND)

        # TODO: add serialization and recalculate rating
        if not request.data:
            return error_response(
                'Invalid data for review creation.',
                status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {'detail': 'TODO: add serialization'},
            status=status.HTTP_201_CREATED,
        )


class PartReviewDetail(APIView):
    # TODO: add permissions

    def get_object(self, pk):
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return None

    def delete(self, request, pk):
        review = self.get_object(pk)
        if review is None:
            return error_response(f'Review with ID {pk} not found.', status.HTTP_404_NOT_FOUND)
        # TODO: check author or admin
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BuildList(APIView):
    # TODO: add permissions

    def get(self, request):
        builds = Build.objects.all().order_by('-created_at')
        user_id = request.query_params.get('user_id')
        if user_id:
            builds = builds.filter(author_id=user_id)
        # TODO: filter private builds and add serialization
        return Response(
            list(builds.values(
                'id', 'title', 'author__username', 'total_price', 'total_tdp', 'recommended_psu_watts', 'is_public', 'created_at'
            )),
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        # TODO: add serialization and compatibility check
        if not request.data:
            return error_response(
                'Invalid data for build creation.',
                status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {'detail': 'TODO: add serialization'},
            status=status.HTTP_201_CREATED,
        )


class BuildDetail(APIView):
    # TODO: add permissions

    def get_object(self, pk):
        try:
            return Build.objects.get(pk=pk)
        except Build.DoesNotExist:
            return None

    def get(self, request, pk):
        build = self.get_object(pk)
        if build is None:
            return error_response(f'Build with ID {pk} not found.', status.HTTP_404_NOT_FOUND)
        # TODO: check access and add serialization
        return Response(
            {
                'id': build.id,
                'title': build.title,
                'author': build.author.username,
                'total_price': build.total_price,
                'total_tdp': build.total_tdp,
                'recommended_psu_watts': build.recommended_psu_watts,
                'is_public': build.is_public,
                'items': list(build.items.values('part_id', 'part__title', 'quantity')),
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk):
        build = self.get_object(pk)
        if build is None:
            return error_response(f'Build with ID {pk} not found.', status.HTTP_404_NOT_FOUND)
        # TODO: check author, compatibility and add serialization
        if not request.data:
            return error_response(
                'Invalid data for build update.',
                status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {'detail': 'TODO: add serialization'},
            status=status.HTTP_200_OK,
        )

    def patch(self, request, pk):
        build = self.get_object(pk)
        if build is None:
            return error_response(f'Build with ID {pk} not found.', status.HTTP_404_NOT_FOUND)
        # TODO: check author and add serialization
        if not request.data:
            return error_response(
                'Invalid data for build update.',
                status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {'detail': 'TODO: add serialization'},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):
        build = self.get_object(pk)
        if build is None:
            return error_response(f'Build with ID {pk} not found.', status.HTTP_404_NOT_FOUND)
        # TODO: check author
        build.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BuildCompare(APIView):
    def get(self, request):
        ids_param = request.query_params.get('ids', '')
        if not ids_param:
            return error_response('Query parameter ids is required.', status.HTTP_400_BAD_REQUEST)

        try:
            build_ids = [int(item.strip()) for item in ids_param.split(',') if item.strip()]
        except ValueError:
            return error_response('Build IDs must be integers.', status.HTTP_400_BAD_REQUEST)

        builds = Build.objects.filter(id__in=build_ids)
        # TODO: add serialization
        return Response(
            list(builds.values(
                'id', 'title', 'total_price', 'total_tdp', 'recommended_psu_watts'
            )),
            status=status.HTTP_200_OK,
        )


class BuildShare(APIView):
    def get(self, request, share_token):
        try:
            build = Build.objects.get(share_token=share_token)
        except Build.DoesNotExist:
            return error_response('Shared build not found.', status.HTTP_404_NOT_FOUND)

        # TODO: add serialization
        return Response(
            {
                'id': build.id,
                'title': build.title,
                'author': build.author.username,
                'total_price': build.total_price,
                'total_tdp': build.total_tdp,
                'recommended_psu_watts': build.recommended_psu_watts,
                'items': list(build.items.values('part_id', 'part__title', 'quantity')),
            },
            status=status.HTTP_200_OK,
        )
