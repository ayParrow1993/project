import './NewsPanel.css';

import Auth from '../Auth/Auth';
import React from 'react';
import NewsCard from '../NewsCard/NewsCard';
import _ from 'lodash';

class NewsPanel extends React.Component{
	constructor(){
		super();
		this.state = {news:null};
	}

	componentDidMount(){
		this.loadMoreNews();
		this.loadMoreNews = _.debounce(this.loadMoreNews, 1000);
		window.addEventListener('scroll',()=>this.handleScroll());
	}

	handleScroll(){
		let scrollY = window.scrollY || window.pageYOffset || document.documentElement.scrollTop;
		if ((window.innerHeight + scrollY) >= (document.body.offsetHeight - 50)){
			console.log('loading more news.');
			this.loadMoreNews();
		}
	}

	loadMoreNews(){
		console.log('actually triggered loading more news');
		const news_url = 'http://'+window.location.hostname+':3000/news';
		const request = new Request(news_url, {
			method:'GET',
			headers: {
				'Authorization':'bearer'+Auth.getToken(),
			}
		});

		fetch(request)
			.then(res=> res.json())
			.then(news => {
				this.setState({
					news:this.state.news ? this.state.news.concat(news) : news,
				})
			});
		
	}

	renderNews(){
		const news_list = this.state.news.map(one_news =>{
			return (
				<a className = 'list-group-item' key={one_news.digest} href="#">
					<NewsCard news={one_news} />
				</a>
			);
		});

		return(
			<div className= 'container_fluid'>
				<div className='list-group'>
					{news_list}
				</div>
			</div>
		);
	}

	render(){
		if(!this.state.news){
			return(
				<div id='msg-app-loading'>
					loading...
				</div>
			);
		}else{
			return(
			<div>
				{this.renderNews()}
			</div>
			);
		}
	}
}
export default NewsPanel;
