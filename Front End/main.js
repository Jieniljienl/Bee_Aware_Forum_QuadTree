// main.js
import React from 'react';

const main = () => {
    const hot_posts = [
        { title: 'Question 1', NumOfLikes: 10, NumOfView: 100 },
        { title: 'Question 2', NumOfLikes: 15, NumOfView: 150 },
        { title: 'Question 3', NumOfLikes: 8, NumOfView: 80 },
      ];
      const questions = [
        // Sample question data
        {
          title: 'Sample Question 1',
          content: 'This is the content of the sample question 1',
          author: { username: 'JohnDoe' },
          create_Time: '2023-08-07',
          NumOfView: 100,
          NumOfLikes: 50,
          id: 1,
        },
        {
          title: 'Sample Question 2',
          content: 'This is the content of the sample question 2',
          author: { username: 'JaneSmith' },
          create_Time: '2023-08-07',
          NumOfView: 75,
          NumOfLikes: 30,
          id: 2,
        },
        // Add more question objects as needed
      ];
      return (
        <div>
          <nav className="navbar navbar-inverse">
          <div class="container-fluid">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
    
                <a class="navbar-brand" href="#">Bee Aware Forum</a>
            </div>
            <div class="collapse navbar-collapse" id="myNavbar">
                <ul class="nav navbar-nav">
                    <li class="active"><a href="{{ url_for('qa.index') }}">Homepage</a></li>
                    <li><a href="{{ url_for('qa.public_my_post') }}">My post</a></li>
                    <li><a href="{{ url_for('qa.save') }}">My save</a></li>
                    <li><a href="{{ url_for('qa.public_qa') }}">post</a></li>
                </ul>
    
    
                <button type="button" class="btn btn-primary me-2"
                        style="float:right;background-color:firebrick;color: white;"><a href="{{ url_for('auth.login') }}">Log
                    in</a></button>
                <button type="button" class="btn btn-success"
                        style="float:right;background-color: darkgoldenrod;color: white;"><a
                        href="{{ url_for('auth.register') }}">Register</a></button>
                <div class="btn-group">
                    <button type="button" class="btn btn-default dropdown-toggle"
                            style="float:right; background-color: black; color: gray;" data-toggle="dropdown"
                            aria-haspopup="true" aria-expanded="false">
                        My Account <span class="caret"></span></button>
                    <ul class="dropdown-menu">
                        <li><a href="{{ url_for('qa.history') }}">History</a></li>
                        <li role="separator" class="divider"></li>
                        <li><a href="{{ url_for('qa.profile') }}">User account</a></li>
                    </ul>
                </div>
            </div>
        </div>
    
        <form class="navbar-form navbar-left" role="search" method="GET" action="{{ url_for('qa.searchinhome') }}">
            <div class="form-group">
                <input type="text" class="form-control" placeholder="Search" name="q"></input>
            </div>
            <button type="submit" class="btn btn-default">Submit</button>
        </form>
          </nav>
          <div style={{ textAlign: 'center' }}>
            <h1><b>Bee Forum</b></h1>
          </div>
          <br />
          <br />
          <div className="container">
            <div className="row">
              <div className="col-sm-4">
                <form method="POST" action="{{ url_for('qa.index') }}">
                  <h2>Hot post</h2>
                  <button type="submit" name="functionality" value="likes" autoFocus>Likes</button>
                  <button type="submit" name="functionality" value="view">View</button>
                  <ul>
                      {/* 显示点赞前三的 hot post */}
                      {hot_posts.slice(0, 3).map((question, index) => (
                      <li key={index}>
                      <h3>#{question.title}:</h3>
                      <h3>likes: {question.NumOfLikes} / view: {question.NumOfView}</h3>
                      </li>
                    ))}
                  </ul>
                </form>
                <hr className="hidden-sm hidden-md hidden-lg" />
              </div>
              <div class="dropdown" style='float: right;font-size: larger;'>
                <button class="btn btn-default dropdown-toggle" type="button" id="dropdownMenu1" data-toggle="dropdown"
                        aria-haspopup="true" aria-expanded="true">
                    category
                    <span class="caret"></span>
                </button>
                <ul class="dropdown-menu" aria-labelledby="dropdownMenu1">
                    <li class="active"><a href="#">000</a></li>
                    <li><a href="#">111</a></li>
                    <li><a href="#">222</a></li>
                    <li role="separator" class="divider"></li>
                    <li><a href="#">Other</a></li>
                </ul>
            </div>
          </div>
    
                <div className="col-sm-8">
          <br />
          <br />
          <ul className="question-ul">
            {questions.map((question) => (
              <li key={question.id}>
                <table width="100%" border="0%">
                  <td colSpan="0" style={{ backgroundColor: 'ghostwhite' }}>
                    <h1>{question.title}</h1>
                    <a href={`/qa/qa_like/${question.id}`} style={{ float: 'right' }}>
                      Like
                    </a>
                    <br />
                    <a href={`/qa/qa_dislike/${question.id}`} style={{ float: 'right' }}>
                      Dislike
                    </a>
                    <h3>{question.content}</h3>
                    <br />
                    <div>
                      <p style={{ fontSize: 'larger' }}>Author: {question.author.username}</p>
                      <p style={{ fontSize: 'larger' }}>Date: {question.create_Time}</p>
                      <p style={{ fontSize: 'larger' }}>view: {question.NumOfView}</p>
                      <p style={{ fontSize: 'larger' }}>likes: {question.NumOfLikes}</p>
                      <br />
                      <p>
                        <a href={`/qa/qa_clicksave/${question.id}`} className="btn btn-primary btn-lg" role="button" style={{ float: 'right' }}>
                          Save
                        </a>
                      </p>
                      <br />
                      <script>
                        {`function confirmSave() {
                          var result = window.confirm("Save the post");
                          if (result) {
                            // Handle save action here
                          }
                        }`}
                      </script>
                      <br />
                      <p>
                        <a className="btn btn-primary btn-lg" href={`/qa/qa_detail/${question.id}`} role="button" style={{ float: 'right' }}>
                          Learn more about it
                        </a>
                      </p>
                      <br />
                      <br />
                    </div>
                  </td>
                </table>
              </li>
            ))}
          </ul>
        </div>
    
    
        <div>
          <div className="jumbotron text-center" style={{ marginBottom: 0 }}>
            <nav aria-label="Page navigation">
              <ul className="pagination">
                <div className="jumbotron text-center" style={{ marginBottom: 0 }}>
                  <nav aria-label="Page navigation">
                    <ul className="pagination">
                      {questions.has_prev && (
                        <li>
                          <a href={`/qa/index?page=${questions.prev_num}`} aria-label="Previous">
                            <span aria-hidden="true">&laquo;</span>
                          </a>
                        </li>
                      )}
    
                      {questions.iter_pages({ left_edge: 1, right_edge: 1, left_current: 1, right_current: 2 }).map((page_num) => (
                        <React.Fragment key={page_num}>
                          {page_num && questions.page === page_num ? (
                            <li className="active">
                              <span>{page_num}</span>
                            </li>
                          ) : (
                            <li>
                              <a href={`/qa/index?page=${page_num}`}>{page_num}</a>
                            </li>
                          )}
                        </React.Fragment>
                      ))}
    
                      {questions.has_next && (
                        <li>
                          <a href={`/qa/index?page=${questions.next_num}`} aria-label="Next">
                            <span aria-hidden="true">&raquo;</span>
                          </a>
                        </li>
                      )}
                    </ul>
                  </nav>
                </div>
              </ul>
            </nav>
          </div>
        </div>
      </div>
    </div>
      );
}

export default main;
