from sklearn.metrics.pairwise import cosine_similarity


#입력받은 collection list의 예측점수 계산
def get_est_ratings(collections:list):
    testset = [('new_user', item, 0) for item in collections]
    svd_model = load_svd_model() 
    predictions = svd_model.test(testset)
    return predictions


#유사한 유저를 찾기
def get_similar_users(user_id, testset):
    # 사용자의 아이템 평점 벡터 생성
    user_vector = np.zeros(testset.n_items)
    for item_id, rating in testset.ur[testset.to_inner_uid(user_id)]:
        user_vector[item_id] = rating

    similarities = []

    # 다른 모든 사용자와의 유사도 계산
    for other_user_id in testset.all_users():
        other_vector = np.zeros(testset.n_items)
        for item_id, rating in testset.ur[other_user_id]:
            other_vector[item_id] = rating

        similarity = cosine_similarity([user_vector], [other_vector])[0][0]
        similarities.append((testset.to_raw_uid(other_user_id), similarity))

    # 유사도가 높은 순으로 정렬
    similar_users = sorted(similarities, key=lambda x: x[1], reverse=True)
    
    return [user[0] for user in similar_users]



# 주어진 사용자와 가장 유사한 사용자의 아이템 추천
def get_recommendations_for_similar_user(user_id, model, testset):

    similar_users = get_similar_users(user_id, testset)
    most_similar_user = similar_users[1]  # 0번은 본인. 

    current_user_items = set([testset.to_raw_iid(item_id) for item_id, _ in testset.ur[testset.to_inner_uid(user_id)]])

    items = []
    for item_id, rating in testset.ur[testset.to_inner_uid(most_similar_user)]:
        raw_item_id = testset.to_raw_iid(item_id)
        
        # 현재 사용자가 아직 평가하지 않은 아이템만 선택합니다.
        if raw_item_id not in current_user_items:
            items.append((raw_item_id, rating))

    # 평점이 높은 아이템 순으로 정렬
    recommended_items = sorted(items, key=lambda x: x[1], reverse=True)
    
    return [item[0] for item in recommended_items]