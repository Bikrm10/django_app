import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from rest_framework.decorators import api_view

df = pd.read_csv("hr.csv")
features = ['Price', 'Type', 'Rating']
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[features])

kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X_scaled)
df['cluster'] = kmeans.labels_
def recommend_hotels(price_range, hotel_type, rating):
    user_data = pd.DataFrame([[price_range, hotel_type, rating]], columns=features)
    user_data_scaled = scaler.transform(user_data)
    cluster_label = kmeans.predict(user_data_scaled)[0]
    recommended_hotels = df[df['cluster'] == cluster_label]
    return recommended_hotels

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ClusteringDataSerializer

from rest_framework import status

@api_view(['POST'])
def clustering_predict_view(request):
    serializer = ClusteringDataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # Extract data from the serializer
    data = serializer.validated_data

    # Call the recommend_hotels function
    recommended_hotels = recommend_hotels(data['price'], data['type'], data['rating'])

    # Convert the recommended hotels DataFrame to a list of dictionaries
    recommended_hotels_list = recommended_hotels.to_dict(orient='records')

    return Response(recommended_hotels_list, status=status.HTTP_200_OK)

