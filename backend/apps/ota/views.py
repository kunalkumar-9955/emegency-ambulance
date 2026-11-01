from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdminPanelRequest, IsSuperAdmin
from apps.ota.models import OTAUpdate


class OTACheckView(APIView):
    permission_classes = []  # Public for mobile apps

    def get(self, request):
        app_name = request.query_params.get("app", "patient")
        platform = request.query_params.get("platform", "android")
        current_build = int(request.query_params.get("build", 0))

        update = (
            OTAUpdate.objects.filter(
                app_name=app_name,
                platform__in=[platform, "all"],
                is_active=True,
                is_rolled_back=False,
                build_number__gt=current_build,
            )
            .order_by("-build_number")
            .first()
        )
        if not update:
            return Response({"update_available": False})
        return Response({
            "update_available": True,
            "version": update.version,
            "build_number": update.build_number,
            "update_type": update.update_type,
            "download_url": update.download_url,
            "changelog": update.changelog,
            "force": update.update_type == "critical",
        })


class OTAPushView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin, IsAdminPanelRequest]

    def post(self, request):
        update = OTAUpdate.objects.create(
            app_name=request.data["app_name"],
            version=request.data["version"],
            build_number=request.data["build_number"],
            platform=request.data.get("platform", "all"),
            update_type=request.data.get("update_type", "optional"),
            download_url=request.data["download_url"],
            changelog=request.data.get("changelog", ""),
            pushed_by=request.user.id,
        )
        return Response({"id": str(update.id)}, status=status.HTTP_201_CREATED)


class OTARollbackView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin, IsAdminPanelRequest]

    def post(self, request, id):
        update = OTAUpdate.objects.get(id=id)
        update.is_rolled_back = True
        update.is_active = False
        update.save()
        return Response({"status": "rolled_back"})
