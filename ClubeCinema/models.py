from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Profile(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    FavMovieGenre = models.CharField(max_length=254)
    UserLevel = models.IntegerField(default=0)
    CreatedAt = models.DateTimeField(default=timezone.now)
    NumberOfRatings = models.IntegerField(default=0)

    def __str__(self):
        return f"<User Name={self.User.username} Email={self.User.email} FavMovieGenre={self.FavMovieGenre} UserLevel={self.User.is_superuser}|{self.UserLevel} >"

    def updateRatingVariables(self):
        self.NumberOfRatings = len(Rating.objects.filter(Profile_id=self.id))
        self.save()

    def delete(self, *args, **kwargs):
        super(Profile, self).delete(self, *args, **kwargs)
        Rating.objects.filter(Profile=self).delete()



class Movie(models.Model):
    ShortName = models.CharField(max_length=25)
    FullName = models.CharField(max_length=100)
    Description = models.CharField(max_length=500)
    AverageRating = models.FloatField(default=0.0)
    NumberOfRatings = models.IntegerField(default=0)
    Genres = models.CharField(max_length=399)  # json array
    MovieLength = models.IntegerField()  # IN SECONDS
    ReleaseDate = models.DateTimeField()

    def __str__(self):
        return f"<Movie ShortName={self.ShortName} AverageRating={self.AverageRating} NumberOfRatings={self.NumberOfRatings} MovieLength={self.MovieLength} ReleaseDate={self.ReleaseDate} >"

    @property
    def getMovieLength(self):
        hours = self.MovieLength // 3600
        minutes = (self.MovieLength - hours*3600) // 60
        return f"{hours}h {minutes}m"

    def updateRatingVariables(self):
        sum, all = 0, Rating.objects.filter(Movie_id=self.id)
        if all:
            for rate in all:
                sum += rate.Rating
            print(all)
            print(sum, len(all), round(sum / len(all), 1))
            self.AverageRating = round(sum / len(all), 1)
            self.NumberOfRatings = len(all)
        else:
            self.AverageRating = 0
            self.NumberOfRatings = 0
        self.save()

    def delete(self, *args, **kwargs):
        super(Movie, self).delete(*args, **kwargs)
      # Profile.updateRatingVariables()


class Rating(models.Model):
    Movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    Profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    Description = models.CharField(
        max_length=700, default=None, blank=True, null=True)
    Rating = models.IntegerField()
    RatedAt = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"<Rating MovieName={self.Movie.ShortName} UserName={self.Profile.User.username} Rating={self.Rating} RatedAt={self.RatedAt}>"

    # Override save method to save as normal and then
    # update the rating variables calling the movie.updateRatingVariables function
    def save(self, *args, **kwargs):
        super(Rating, self).save(*args, **kwargs)
        self.Movie.updateRatingVariables()
        self.Profile.updateRatingVariables()

    def delete(self, *args, **kwargs):
        super(Rating, self).delete(*args, **kwargs)
        self.Movie.updateRatingVariables()
        self.Profile.updateRatingVariables()
