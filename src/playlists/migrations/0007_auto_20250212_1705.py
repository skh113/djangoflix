# Generated by Django 3.2.25 on 2025-02-12 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("videos", "0013_alter_video_video_id"),
        ("playlists", "0006_remove_playlist_videos"),
    ]

    operations = [
        migrations.CreateModel(
            name="PlaylistItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("order", models.IntegerField(default=1)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "playlist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="playlists.playlist",
                    ),
                ),
                (
                    "video",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="videos.video"
                    ),
                ),
            ],
            options={
                "ordering": ["order", "-created"],
            },
        ),
        migrations.AddField(
            model_name="playlist",
            name="videos",
            field=models.ManyToManyField(
                blank=True,
                related_name="playlist_item",
                through="playlists.PlaylistItem",
                to="videos.Video",
            ),
        ),
    ]
