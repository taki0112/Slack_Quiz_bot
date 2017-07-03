from slackclient import SlackClient
import random
API_TOKEN = "xoxb-207833593190-iEmKb7YbJNtKWXDUM9Wp5fQK"
slack_client = SlackClient(API_TOKEN)

def parse_slack(msg, quiz_dict):
    quiz_text = random.choice(list(quiz_dict.keys()))
    output_list = msg
    # print(output_list)
    # print(len(output_list))
    if output_list and len(output_list) > 0:
        for output in output_list:
            # print(output)

            if output and 'text' in output and 'bot_id' not in output:
                command = output['text']
                if command.__contains__("퀴즈") :
                    slack_client.api_call(
                        "chat.postMessage",
                        channel=output['channel'],
                        text=quiz_text,
                        username='Quiz_bot',
                        icon_emoji=':ghost:'
                    )


                    check_answer(quiz_dict, quiz_text)



def check_answer(quiz_dict, quiz_text) :
    if slack_client.rtm_connect():
        print("Connected!")
        while True :
            output_list = slack_client.rtm_read()


            if output_list and len(output_list) > 0:

                for output in output_list :
                    if output and 'text' in output and 'bot_id' not in output :
                        answer = output['text']
                        if quiz_dict.__contains__(quiz_text) :
                            if quiz_dict[quiz_text].__eq__(answer) :
                                slack_client.api_call(
                                    "chat.postMessage",
                                    channel=output['channel'],
                                    text="정답입니다.",
                                    username='Quiz_bot',
                                    icon_emoji=':ghost:'
                                )
                                return 0
                            elif not quiz_dict[quiz_text].__eq__(answer) :
                                slack_client.api_call(
                                    "chat.postMessage",
                                    channel=output['channel'],
                                    text="틀렸습니다.",
                                    username='Quiz_bot',
                                    icon_emoji=':ghost:'
                                )
                                return 0


    else:
        print("Connection failed.")


def quiz_mapping() :
    with open("Quiz.txt", 'r') as f :
        quiz_dict = dict()
        lines = f.readlines()
        for line in lines :
            quiz = line.split("/")[0]
            answer = line.split("/")[1].strip()
            quiz_dict[quiz] = answer

    return quiz_dict

if __name__ == "__main__":
    quiz_dict = quiz_mapping()
    if slack_client.rtm_connect():
        print("Connected!")
        while True :
            parse_slack(slack_client.rtm_read(), quiz_dict)
            # if quiz_text is not None :
            #     print(quiz_text)
            #     check_answer(quiz_dict, quiz_text)

    else:
        print("Connection failed.")