import random
import time
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def upward(score):
    max_value = max(score)  # 리스트에서 가장 큰 값을 찾습니다.
    for i in range(len(score)):
        if i>8:
            if score[i] == 0:
                score[i] = max_value
    




def simulate_game(team1, team2):
    score1 = [0 for _ in range(13)]
    score2 = [0 for _ in range(13)]
    placeholder = st.empty()
    for inning in range(1, 13):
        if inning >9:
            if score_data.at[0,'총점'] !=score_data.at[1,'총점']:
                break
            else:
                if inning >10:
                    if score_data.at[0,'총점'] !=score_data.at[1,'총점']:
                        break
                    else:
                        if inning >11:
                            if score_data.at[0,'총점'] !=score_data.at[1,'총점']:
                                break
        if random.random()<team1_win_rate:
            team1_runs = random.randint(0, 2)
        else:
            team1_runs = 0
        score_data.at[0,f'{inning}']=team1_runs
        score_data.at[0,'총점'] += team1_runs
        score1[inning]=score_data.at[0,'총점']
        placeholder.write(score_data)
        time.sleep(0.3)

        if inning==9 and score_data.at[0,'총점'] <score_data.at[1,'총점']:
            placeholder.write(score_data)
            break

        if random.random()<team2_win_rate:
            team2_runs = random.randint(0, 2)
        else:
            team2_runs = 0
        score_data.at[1,f'{inning}']=team2_runs
        score_data.at[1,'총점'] += team2_runs
        score2[inning]=score_data.at[1,'총점']
        
        placeholder.write(score_data)
        time.sleep(0.3)

    st.write("게임 종료!")
    st.write(f"{team1['name']}:",str(score_data.at[0,'총점']),"점",f"{team2['name']}:" ,str(score_data.at[1,'총점']),"점")
    if int(score_data.at[0,'총점'])>int(score_data.at[1,'총점']):
        st.write(f"{team1['name']}: 승리!")
    elif int(score_data.at[0,'총점'])<int(score_data.at[1,'총점']):
        st.write(f"{team2['name']}: 승리!")
    else:
        st.write("비겼습니다!")

    upward(score1)
    upward(score2)
    fig, ax = plt.subplots()
    plt.plot(score1[0:13],color="#FFBF00")
    plt.plot(score2[0:13],color="#FF8000")
    plt.xlabel('inning')
    plt.ylabel('score')
    ax.set_xticks(range(0, 13, 1))
    ax.set_yticks(range(0,15,1))
    plt.gca().spines['left'].set_position(('data', 0))
    plt.gca().spines['bottom'].set_position(('data', 0))
    plt.tick_params(axis='y', direction='inout', which='both', length=0)
    plt.grid(True)
    st.pyplot(fig)






selected = st.sidebar.selectbox("목차", ("팀 기록","팀 비교", "야구시뮬레이션"))
st.header('야구 분석 프로젝트')
team_data = pd.read_csv('team.csv')
team = team_data["team"].unique()
if selected == '팀 기록':
    select_team = st.selectbox(" 팀을 선택하세요", team,placeholder="Select team...")
    st.write('승리,패배,무승부')
    #승리,패배,무승부
    win_or_lose_data = pd.DataFrame(
        {
            "year": team_data[team_data['team'] == select_team]["year"],
            "win": team_data[team_data['team'] == select_team]["win"],
            "lose": pd.array(team_data[team_data['team'] == select_team]["lose"])*(-1),
            "draw": team_data[team_data['team'] == select_team]["draw"],
        }
    )
    st.bar_chart(win_or_lose_data, x="year", y=["win","lose","draw"],color=["#DFFDFE","#FA5858","#2E64FE"])

    #승률
    st.write("승률")
    Winning_Percentage_data = pd.DataFrame(
        {
        "year": team_data[team_data['team'] == select_team]["year"],
        "Winning Percentage": team_data[team_data['team'] == select_team]["Winning Percentage"],
        }
    )
    st.line_chart(Winning_Percentage_data, x="year", y="Winning Percentage", color="#82FA58")


    #정규랭킹과 최종랭킹
    st.write('정규랭킹와 최종랭킹')
    fig, ax = plt.subplots()

    year = team_data[team_data['team'] == select_team]["year"]
    regular_ranking = team_data[team_data['team'] == select_team]["regular ranking"]
    final_ranking = team_data[team_data['team'] == select_team]["final ranking"]

    plt.plot(year, regular_ranking, label='Regular Ranking',color="#FFBF00",marker="o")
    plt.plot(year, final_ranking, label='Final Ranking',color="#FF8000",marker="o")
    plt.xlabel('Year')
    plt.ylabel('Ranking')
    plt.title('Ranking over the Years')
    plt.xticks(range(int(min(year)), int(max(year)) + 1),rotation=45)
    plt.ylim(10, 0)
    plt.yticks(range(11))
    plt.gca().set_yticklabels([str(i) if i != 0 else '' for i in range(11)])
    for tick in ax.get_yticks():
        ax.axhline(y=tick, color='gray', linestyle='--', linewidth=0.5)
    st.pyplot(fig)



if selected == '팀 비교':
    select_team1 = st.selectbox('비교할 서로 다른 두 팀을 선택하세요',team,placeholder="Select team...",key='team1_selectbox')
    select_team2 = st.selectbox('',team,index=1,key='team2_selectbox',label_visibility='collapsed')
    if select_team1 == select_team2:
        st.error("서로 다른 팀을 선택하세요.",icon="🚨")
    else:
        st.write("연도별 승률 비교")
        team1_data = team_data[team_data['team'] == select_team1][['year', 'Winning Percentage']]
        team2_data = team_data[team_data['team'] == select_team2][['year', 'Winning Percentage']]

        min_year = min(team1_data['year'].min(), team2_data['year'].min())
        max_year = max(team1_data['year'].max(), team2_data['year'].max())

        team1_data = team1_data.set_index('year').reindex(range(min_year, max_year + 1)).reset_index()
        team2_data = team2_data.set_index('year').reindex(range(min_year, max_year + 1)).reset_index()

        merged_data = pd.merge(team1_data, team2_data, on='year', suffixes=('_1', '_2'))
        st.line_chart(merged_data.set_index('year').rename(columns={'Winning Percentage_1': select_team1, 'Winning Percentage_2': select_team2}))



        st.write('평균 정규랭킹와 최종랭킹')
        fig, ax = plt.subplots()

        team1_regular_ranking = team_data[team_data['team'] == select_team1]["regular ranking"]
        team1_final_ranking = team_data[team_data['team'] == select_team1]["final ranking"]
        team2_regular_ranking = team_data[team_data['team'] == select_team2]["regular ranking"]
        team2_final_ranking = team_data[team_data['team'] == select_team2]["final ranking"]

        avg_team1_regular_ranking = team1_regular_ranking.mean()
        avg_team2_regular_ranking = team2_regular_ranking.mean()
        avg_team1_final_ranking = team1_final_ranking.mean()
        avg_team2_final_ranking = team2_final_ranking.mean()


        team=[f'{select_team1}',f'{select_team2}']
        x = range(len(team))
        y1=[avg_team1_regular_ranking,avg_team2_regular_ranking ]
        y2=[avg_team1_final_ranking, avg_team2_final_ranking]

        plt.scatter(x, y1, label='regular ranking', color='#FFBF00')
        plt.scatter(x, y2, label='final ranking', color='#FF8000')
        plt.xticks(x, team)
        plt.ylim(10,0)
        plt.yticks(range(10, -1, -1)) 
        plt.yticks(range(11))
        plt.gca().set_yticklabels([str(i) if i != 0 else '' for i in range(11)])
        for tick in ax.get_yticks():
            ax.axhline(y=tick, color='gray', linestyle='--', linewidth=0.5)
        ax.set_xlim(-2, 3)
        for i, txt in enumerate(y1):
            ax.text(x[i], txt-0.5, f'{txt:.2f}', ha='center', color='#FFBF00')
        for i, txt in enumerate(y2):
            ax.text(x[i], txt+0.5, f'{txt:.2f}', ha='center', color='#FF8000')
        plt.legend()
        st.pyplot(fig)


if selected == '야구시뮬레이션':
    st.header('야구시뮬레이션')
    wr_2024_data=pd.read_csv('2024.csv')
    wr_2023_data=pd.read_csv('2023.csv')
    wr_2022_data=pd.read_csv('2022.csv')
    score_data = pd.read_csv('score.csv')
    score1=[]
    score2=[]
    Game=False
    select_year = st.selectbox(" 연도를 선택하세요", ['2024','2023','2022'],placeholder="Select team...")
    if select_year== '2024':
        wr_data=wr_2024_data
    elif select_year=='2023':
        wr_data=wr_2023_data
    else:
        wr_data=wr_2022_data

    team = wr_data["team"].unique()
    select_team1 = st.selectbox('대결할 두 팀을 고르세요',team,key='team1')
    select_team2 = st.selectbox('',team,index=1,key='team2_selectbox',label_visibility='collapsed')
    if select_team1 == select_team2:
        st.error("서로 다른 팀을 선택하세요.",icon="🚨")
    else:
        team1_name = select_team1
        wr1=wr_data[wr_data['team']==select_team1][select_team2]
        team1_wr=wr1.str.split('-').tolist()
        team1_wr = [int(item) for sublist in team1_wr for item in sublist]
        team1_win_rate = round(int(team1_wr[0])/(int(team1_wr[0])+int(team1_wr[1])+int(team1_wr[2])),2)
        team1 = {
            "name":select_team1,
            "win_rate":team1_win_rate,
            "runs":0,
        }

        team2_name = select_team2
        wr2=wr_data[wr_data['team']==select_team2][select_team1]
        team2_wr=wr2.str.split('-').tolist()
        team2_wr = [int(item) for sublist in team2_wr for item in sublist]
        team2_win_rate =round(int(team2_wr[0])/(int(team2_wr[0])+int(team2_wr[1])+int(team2_wr[2])),2)
        team2 = {
            "name":select_team2,
            "win_rate":team2_win_rate,
            "runs":0,
        }

        score_data['team']=[f'{team1['name']}',f'{team2['name']}']
        st.write(f"{select_team1}의 승률:",team1_win_rate)
        st.write(f"{select_team2}의 승률:",team2_win_rate)

        if st.button("Game Start", type="primary"):
            Game=True
        if Game==True:    
            total_runs = simulate_game(team1, team2)
            if st.button("reset",type="primary"):
                Game=False
        
